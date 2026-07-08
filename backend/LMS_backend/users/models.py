from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        unique=True, #Every user must have a unique email.
        help_text="Each user must have a unique email address."
    )

    full_name = models.CharField(
        max_length=150
    )

