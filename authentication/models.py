from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    course_interest = models.CharField(max_length=255, blank=True)
    highest_education = models.CharField(max_length=255)  
    percentage = models.FloatField(null=True, blank=True)
    start_study = models.DateField()
    receive_newsletter = models.BooleanField(default=False)
    receive_promo_offers = models.BooleanField(default=False)
    have_passport = models.BooleanField(default=False)


    # Fields for OTP and Google Auth
    otp_enabled = models.BooleanField(default=False)
    otp_secret_key = models.CharField(max_length=100, blank=True, null=True)
    google_auth_enabled = models.BooleanField(default=False)
    google_auth_secret_key = models.CharField(max_length=16, blank=True, null=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username