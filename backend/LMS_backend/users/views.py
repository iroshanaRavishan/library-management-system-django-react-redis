from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)

from rest_framework import generics


class UserListView(generics.ListAPIView):
    # List all users.

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]



class UserDetailView(generics.RetrieveAPIView):
    # Retrieve a single user.

    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated] # Only logged-in users can access this API.



class RegisterView(generics.CreateAPIView):
    # Register a new user.

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]