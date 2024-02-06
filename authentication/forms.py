from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser


# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, required=True)
#     phone = forms.CharField(required=True)  # Assuming phone is not required for now
#     course_interest = forms.CharField(required=False)
#     username = forms.CharField(required=True)
#     email = forms.EmailField(required=True) 

#     class Meta:
#         model = CustomUser
#         fields = [ 
#             "email",
#             "password",
#             "phone",
#             "course_interest",
#         ]

#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         # user.username = self.cleaned_data[
#         #     "email"
#         # ]  # Set 'username' to the 'email' value
#         if commit:
#             user.save()
#         return user


# class ExtendedRegistrationForm(forms.ModelForm):
#     course_interest = forms.CharField(max_length=255, required=True)
#     highest_education = forms.CharField(
#         max_length=255, required=True
#     )  # You might want to make this a ChoiceField
#     percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
#     start_study = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         required=True
#     )  # Adjust the field type based on your requirements
#     receive_newsletter = forms.BooleanField(required=False)
#     receive_promo_offers = forms.BooleanField(required=False)
#     have_passport = forms.BooleanField(required=False)

#     class Meta:
#         model = CustomUser
#         fields = [
#             "course_interest",
#             "highest_education",
#             "percentage",
#             "start_study",
#             "receive_newsletter",
#             "receive_promo_offers",
#             "have_passport"
#         ]

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    phone = forms.CharField(required=True)
    course_interest = forms.CharField(max_length=255, required=False)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    highest_education = forms.CharField(max_length=255, required=True)
    percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    start_study = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    receive_newsletter = forms.BooleanField(required=False)
    receive_promo_offers = forms.BooleanField(required=False)
    have_passport = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "phone",
            "course_interest",
            "highest_education",
            "percentage",
            "start_study",
            "receive_newsletter",
            "receive_promo_offers",
            "have_passport"
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ResetPassword(forms.ModelForm):
    class Meta:
        model = CustomUser  # Specify the model class
        fields = ['email', 'password']  # Include the fields you want to use in the form
    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=10)

class OTPForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["otp_enabled", "otp_secret_key"]

class GenerateOTPForm(forms.Form):
    phone = forms.CharField(max_length=255, required=True, help_text="Enter your phone number to receive OTP")

class OTPVerificationForm(forms.Form):
    email = forms.CharField(max_length=255, required=True, help_text="Enter your phone number")
    otp = forms.CharField(max_length=6, required=True, help_text="Enter the OTP sent to your phone")




class GoogleAuthForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["google_auth_enabled", "google_auth_secret_key"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
