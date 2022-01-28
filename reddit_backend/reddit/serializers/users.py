import django.contrib.auth.password_validation
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.password_validation import validate_password

from reddit.models import User, UserProfile

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("name",)


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    def validate_password(self, password):
        validate_password(password)
        return password

    class Meta:
        model = User
        fields = ("email", "password", "profile", "id")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, name=profile_data["name"])
        return user


class UserLoginSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password is not found."
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )
        return {"email": user.email, "token": jwt_token}


class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserSerializer()
    class Meta:
        model = User
        fields = ("email", "profile", "id")
