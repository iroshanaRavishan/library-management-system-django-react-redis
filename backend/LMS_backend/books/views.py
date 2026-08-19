from django.shortcuts import render

from rest_framework import generics

from .models import (
    Author,
    Category,
    Publisher,
)

from .serializers import (
    AuthorSerializer,
    CategorySerializer,
)

from .permissions import IsLibrarianOrReadOnly


class AuthorListView(generics.ListCreateAPIView):
    """
    GET  -> List authors
    POST -> Create an author
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    -> Retrieve an author
    PUT    -> Update an author
    PATCH  -> Partially update an author
    DELETE -> Delete an author
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]



class CategoryListView(generics.ListCreateAPIView):
    """
    GET  -> List categories
    POST -> Create a category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLibrarianOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    -> Retrieve a category
    PUT    -> Update a category
    PATCH  -> Partially update a category
    DELETE -> Delete a category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLibrarianOrReadOnly]



class PublisherListView(generics.ListCreateAPIView):
    """
    GET  -> List publishers
    POST -> Create a publisher
    """