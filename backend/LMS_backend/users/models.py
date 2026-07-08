from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Role(models.TextChoices):
        LIBRARIAN = "LIBRARIAN", "Librarian"
        MEMBER = "MEMBER", "Member"

    email = models.EmailField(
        unique=True, #Every user must have a unique email.
        help_text="Each user must have a unique email address."
    )

    full_name = models.CharField(
        max_length=150
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True # making the field isn't mandatory
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    