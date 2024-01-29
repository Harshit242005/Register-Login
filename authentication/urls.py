from django.urls import path, re_path
from .views import RegisterView1, RegisterView2, UserLogin, GoogleAuthSettings, HomePageView, UserLogout, GenerateOTP, VerifyOTP, user_info
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
    path('register/step1/', RegisterView1.as_view(), name='register_step1'),
    path('register/step2/', RegisterView2.as_view(), name='register_step2'),
    path('login/', UserLogin.as_view(), name='login_url'),
    path('home/', HomePageView.as_view(), name='home_url'),
    path('api/user-info/', user_info, name='user-info'),
    path('generate-otp/', GenerateOTP.as_view(), name='generate_otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('logout/', UserLogout.as_view(), name='logout_url'),
    path('google-auth/<int:user_id>/', GoogleAuthSettings.as_view(), name='google-auth-settings'),

    # Swagger documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
