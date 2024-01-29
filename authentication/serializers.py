from rest_framework import serializers
from .models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    # Assuming additional fields from step 2 are part of the CustomUser model
    course_interest = serializers.CharField(max_length=255)
    highest_education = serializers.CharField(max_length=255)  # Update the max_length as needed
    percentage = serializers.FloatField(required=False, allow_null=True)
    start_study = serializers.DateField()  # Use the correct field type as per your model
    receive_newsletter = serializers.BooleanField(required=False, default=False)
    receive_promo_offers = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'course_interest', 'highest_education', 'percentage', 'start_study', 'receive_newsletter', 'receive_promo_offers']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create the user with the validated data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            course_interest=validated_data.get('course_interest', ''),
            highest_education=validated_data.get('highest_education', ''),
            percentage=validated_data.get('percentage', 0),
            start_study=validated_data.get('start_study', None),
            receive_newsletter=validated_data.get('receive_newsletter', False),
            receive_promo_offers=validated_data.get('receive_promo_offers', False),
            phone = validated_data.get('phone', ''),
        )
        return user

class OTPSettingsSerializer(serializers.ModelSerializer):
    otp_secret_key = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['otp_enabled', 'otp_secret_key']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class GoogleAuthSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['google_auth_enabled', 'google_auth_secret_key']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance