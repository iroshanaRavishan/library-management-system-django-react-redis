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