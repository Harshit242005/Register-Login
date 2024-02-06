from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import CustomUser
# ExtendedRegistrationForm
from .forms import RegistrationForm, ResetPassword, LoginForm, GenerateOTPForm,OTPVerificationForm
from .serializers import RegistrationSerializer, OTPSettingsSerializer, GoogleAuthSettingsSerializer
import pyotp
from django.conf import settings
from rest_framework.throttling import UserRateThrottle
from django.core.cache import caches
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.template.loader import render_to_string
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse
import json


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        print(f'request data is: {data}')
        # Validate the incoming data using the custom validation function
        if self.validate_data(data):
            print('register data validated correctly ')
            try:
                user = RegistrationSerializer.create(RegistrationSerializer(), validated_data=data)
                print(f'user object that we have created {user}')
                # Create access and refresh tokens
                token, created = Token.objects.get_or_create(user=user)
                print(f'token that we have created: {token} and created; {created}')
                # Send the correct response to the front-end React application
                return Response({'success': True, 'username': user.username, 'access_token': token.key})
            except IntegrityError:
                print('user already existed')
                return Response({'exist_already': 'A user with this phone number already exists.'})
                
        else:
            print('Registration failed because of invalid data validation')
            # Handle the case where data is not valid
            return Response({'success': False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def validate_data(self, data):
        # Implement your custom validation logic here
        # You can use the same logic as in your form's clean method or add additional checks
        form = RegistrationForm(data)
        if form.is_valid():
            return True
        else:
            # Access detailed error information using form.errors
            print(f'Validation errors: {form.errors}')
            return False


# class RegisterView1(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request):
#         print('getting the request for the register view 1 endpoint')

#     def post(self, request):
#         data = request.data
#         print(f'request data is: {data}')

#         # Validate the incoming data using the custom validation function
#         if self.validate_data(data):
#             # Store the form data in the session
#             request.session['registration_step1_data'] = json.dumps(data)
#             request.session.save()  # Save the session explicitly
#             print(f'request data in the session of request is {request.session}')
#             return Response({'success': True, 'message': 'Stage one data stored successfully'})
#         else:
#             # Handle the case where data is not valid
#             return Response({'success': False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

#     def validate_data(self, data):
#         # Implement your custom validation logic here
#         # You can use the same logic as in your form's clean method or add additional checks
#         form = RegistrationForm(data)
#         if form.is_valid():
#             return True
#         else:
#             # Access detailed error information using form.errors
#             print(f'Validation errors: {form.errors}')
#             return False

# class RegisterView2(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         print(f'request data of the second stage is: {request.data}')
#         print(f'request session is this: {request.session}')
#         request_1_session_data = request.session.get('registration_step1_data')
#         print(f'request session data for the view 2 from view 1 is: {request_1_session_data}')
#         step1_data = json.loads(request.session.get('registration_step1_data', {}))
#         print(f'session data of the register view 1 is: {step1_data}')
#         if step1_data is None:
#             print('registration data from the view 1 does not exist in the session')
#             return Response({'success': False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


#         data = request.data
#         print(f'the data for the register view 2 is: {data}')
#         if self.validate_data(data):
#             combined_data = {**step1_data, **data}
#             print(f'the combined data is: {combined_data}')
#             try:
#                 user = RegistrationSerializer.create(RegistrationSerializer(), validated_data=combined_data)
#                 del request.session['registration_step1_data']
#                 token, created = Token.objects.get_or_create(user=user)
                
#                 # instead send the user data as user name and success message corerctly
#                 username = user['username']
#                 print(f'username from get user is: {username}')
#                 return Response({'success': True, 'username': username})
                
#             except IntegrityError:
#                 return Response({'exist_already': 'A user with this phone number already exists.'})
#         else:
#             print('Second stage user registration failed because of invalid data validation')
#             # Handle the case where data is not valid
#             return Response({'success': False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

#     def validate_data(self, data):
#         # Implement your custom validation logic here
#         form = ExtendedRegistrationForm(data)
#         try:
#             form.is_valid()
#             return True
#         except ValidationError:
#             # Access detailed error information using form.errors
#             print(f'Validation errors: {form.errors}')
#             return False



from .SendMail import send_email

# def send_otp_to_user(otp, phone_number):
#     # Print the OTP to the console (for development purposes)
#     print(f"Sending OTP {otp} to phone number {phone_number}")

class OTPRateThrottle(UserRateThrottle):
    rate = '1/min'  # Adjust as needed

otp_cache = caches[settings.OTP_CACHE_ALIAS]

class GenerateOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        print(f'data for genegrating otp: {data}')
        if self.validate_data(data):
            email = data.get('email')
            otp_secret_key = pyotp.random_base32()
            totp = pyotp.TOTP(otp_secret_key)
            otp = totp.now()
            otp_cache.set(email, otp, timeout=settings.OTP_TTL)
            send_email(email, "Verification OTP", otp)
            return Response({'success': True, 'message': 'OTP generated successfully'})
        else:
            return Response({'email_validation_error': 'This email does not exist as a user go to signup'})
        
    def validate_data(self, data):
        form = GenerateOTPForm(data)
        try: 
            form.is_valid()
            return True
        except ValidationError:
            print(f'Validation errors: {form.errors}')
            return False
        
class NewPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        print(f'new password filling data is: {data}')
        if self.validate_data(data):
            # Change user credentials [password] from the email in the custom user model
            email = data['email']
            new_password = data['password']
        
            # Retrieve the user with the provided email using the model manager
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'success': False, 'message': 'User not found with the provided email'}, status=status.HTTP_404_NOT_FOUND)

            # Change the user's password
            user.set_password(new_password)
            user.save()

            return Response({'success': True, 'message': 'Password changed successfully'})
        else: 
            print('There is some error while changing the password, data is not valid')
            # Handle the case where the data is not valid
            return Response({'success': False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        

    # function to validate data
    def validate_data(self, data):
        form = ResetPassword(data)
        try: 
            form.is_valid()
            return True
        except ValidationError:
            return False



class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # form = OTPVerificationForm(request.POST)
        data = request.data
        print(f'for verifying post data is: {data}')
        if self.validate_data(data):
            email = data['email']
            otp_to_verify = data['otp']
            otp_in_cache = otp_cache.get(email)
            if otp_in_cache and otp_in_cache == otp_to_verify:
                otp_cache.delete(email)
                return Response({'success': True, 'message': 'OTP verified successfully'})
            else:
                return Response({'message': "Invalid OTP"})
        else:
            return Response({'message': 'redirecting back to verify page'})
        
    def validate_data(self, data):
        form = OTPVerificationForm(data)
        try: 
            form.is_valid()
            return True
        except ValidationError:
            print(f'Validation errors: {form.errors}')
            return False

    def delete(self, request):
        email = request.data.get("email")
        otp_cache.delete(email)  # Manually delete the OTP from Redis
        return Response({"message": "OTP deleted successfully"})
    

class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        print(f'login endpoint data is: {data}')
        if self.validate_data(data):
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                # Return a JSON response with tokens and status code 200 (OK)
                return Response({'status': 'success', 'username': username, 'password': password, 'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
            else:
                # Return a JSON response indicating login failure with status code 401 (Unauthorized)
                return Response({'status': 'error', 'message': 'Invalid username or password for login'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Return a JSON response indicating validation failure with status code 400 (Bad Request)
            return Response({'status': 'error', 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            
    def validate_data(self, data):
        form = LoginForm(data)
        try:
            form.is_valid()
            return True
        except ValidationError:
            # Access detailed error information using form.errors
            print(f'Validation errors: {form.errors}')
            return False


class GoogleAuthSettings(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = GoogleAuthSettingsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Google Auth settings updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return render(request, 'authentication/home.html', {'username': request.user.username})



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    return Response({'username': request.user.username})

class UserLogout(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login_url')
    