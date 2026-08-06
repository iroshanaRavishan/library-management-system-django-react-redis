from django.db import models


class Author(models.Model):
    #Stores book author information.

    name = models.CharField(max_length=150, unique=True)

