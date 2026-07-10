from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Used for reading user information

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "full_name",
            "phone_number",
            "role",
        )


class RegisterSerializer(serializers.ModelSerializer):
    # Used when registering a new user

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "full_name",
            "phone_number",
            "role",
        )

    def validate_password(self, value):
        return make_password(value)