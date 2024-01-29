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
from .forms import RegistrationForm, LoginForm, ExtendedRegistrationForm,GenerateOTPForm,OTPVerificationForm
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


class RegisterView1(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Initialize an empty form for a GET request
        form = RegistrationForm()
        return render(request, 'authentication/register_step1.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Store the form data in the session
            request.session['registration_step1_data'] = form.cleaned_data
            return redirect(reverse('register_step2'))
        else:
            # If the form is not valid, render the page with form errors
            return render(request, 'authentication/register_step1.html', {'form': form})


class RegisterView2(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Check if the first step data is in session
        step1_data = request.session.get('registration_step1_data')
        if step1_data is None:
            # Redirect to the first step if the session data is missing
            return redirect(reverse('register_step1'))

        # Initialize an empty form for a GET request
        form = ExtendedRegistrationForm()
        return render(request, 'authentication/register_step2.html', {'form': form})

    def post(self, request):
        step1_data = request.session.get('registration_step1_data')
        if step1_data is None:
            return redirect(reverse('register_step1'))

        form = ExtendedRegistrationForm(request.POST)
        if form.is_valid():
            combined_data = {**step1_data, **form.cleaned_data}
            print(combined_data)
            try:
                user = RegistrationSerializer.create(RegistrationSerializer(), validated_data=combined_data)
                del request.session['registration_step1_data']
                token, created = Token.objects.get_or_create(user=user)
                return redirect('generate_otp')
            except IntegrityError:
                messages.error(request, 'A user with this phone number already exists.')
                return render(request, 'authentication/register_step2.html', {'form': form})
        else:
            return render(request, 'authentication/register_step2.html', {'form': form})

            
def send_otp_to_user(otp, phone_number):
    # Print the OTP to the console (for development purposes)
    print(f"Sending OTP {otp} to phone number {phone_number}")

class OTPRateThrottle(UserRateThrottle):
    rate = '1/min'  # Adjust as needed

otp_cache = caches[settings.OTP_CACHE_ALIAS]

class GenerateOTP(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        form = GenerateOTPForm()
        return render(request, 'authentication/request_otp.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = GenerateOTPForm(request.POST)
        if form.is_valid():
            print("here")
            phone_number = form.cleaned_data['phone']
            otp_secret_key = pyotp.random_base32()
            totp = pyotp.TOTP(otp_secret_key)
            otp = totp.now()
            otp_cache.set(phone_number, otp, timeout=settings.OTP_TTL)
            send_otp_to_user(otp, phone_number)
            print("here")
            return redirect('verify_otp')
        else:
            return render(request, 'authentication/request_otp.html', {'form': form})

class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        form = OTPVerificationForm()
        return render(request, 'authentication/verify_otp.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            otp_to_verify = form.cleaned_data['otp']
            otp_in_cache = otp_cache.get(phone)
            if otp_in_cache and otp_in_cache == otp_to_verify:
                otp_cache.delete(phone)
                # Redirect to the login page after successful OTP verification
                return redirect('login_url')
            else:
                return render(request, 'authentication/verify_otp.html', {'form': form, 'message': "Invalid OTP"})
        else:
            return render(request, 'authentication/verify_otp.html', {'form': form})

    def delete(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        otp_cache.delete(phone)  # Manually delete the OTP from Redis
        return Response({"message": "OTP deleted successfully"})
    

class UserLogin(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                response = redirect('home_url')  # Redirect to home page URL
                response.set_cookie('accessToken', str(refresh.access_token))
                response.set_cookie('refreshToken', str(refresh))
                return response
            else:
                form.add_error(None, 'Invalid username or password.')
                return render(request, 'authentication/login.html', {'form': form})


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
    