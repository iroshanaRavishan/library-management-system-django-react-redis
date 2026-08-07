from django.db import models


class Author(models.Model):
    #Stores book author information.

    name = models.CharField(max_length=150, unique=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    #Stores book categories.

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    # Stores publisher information.

    name = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Stores book information.

    isbn = models.CharField(max_length=20, unique=True)

    title = models.CharField(max_length=255)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books",
    )


    total_copies = models.PositiveIntegerField(default=1)

    available_copies = models.PositiveIntegerField(default=1)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title