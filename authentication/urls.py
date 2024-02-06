from django.urls import path, re_path
from .views import RegisterView,  UserLogin, NewPassword, GoogleAuthSettings, HomePageView, UserLogout, GenerateOTP, VerifyOTP, user_info
# RegisterView2, RegisterView1
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Documentation for the API endpoints",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
   #  path('RegisterStageOne', RegisterView1.as_view(), name='register_step1'),
   #  path('RegisterStageSecond', RegisterView2.as_view(), name='register_step2'),
    path('Register', RegisterView.as_view(), name='register'),


    path('login', UserLogin.as_view(), name='login_url'),
    # an endpoint to listen for the new password filling 
    path('NewPassword', NewPassword.as_view(), name="new_password"),

   #  path('home', HomePageView.as_view(), name='home_url'),
   #  path('api/user-info', user_info, name='user-info'),

   # otp related stuff implementation and handling stuff
    path('GenerateOTP', GenerateOTP.as_view(), name='generate_otp'),
    path('VerifyOTP', VerifyOTP.as_view(), name='verify_otp'),
    # adding some resend otp endpoint for sending the OTP again 
    path('ResendOTP', GenerateOTP.as_view(), name='resend_otp'),

    path('logout', UserLogout.as_view(), name='logout_url'),
    path('google-auth/<int:user_id>', GoogleAuthSettings.as_view(), name='google-auth-settings'),

    # Swagger documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
