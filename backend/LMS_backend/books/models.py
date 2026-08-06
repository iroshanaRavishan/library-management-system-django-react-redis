from django.db import models


class Author(models.Model):
    #Stores book author information.

    name = models.CharField(max_length=150, unique=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

