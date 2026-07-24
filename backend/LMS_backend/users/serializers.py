from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # Serializer used for returning user information.

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "email",
            "full_name",
            "phone_number",
            "role",
        ]

        extra_kwargs = {
            "url": {
                "view_name": "user-detail"
            }
        }


class RegisterSerializer(serializers.ModelSerializer):
    # Serializer responsible for creating a new user.

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "full_name",
            "phone_number",
            "role",
        ]

    def validate_password(self, value):
        # Hash the password before saving it.
        return make_password(value)
    

class LoginSerializer(serializers.Serializer):
    # Serializer used to validate login credentials.

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")
