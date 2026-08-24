from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics

from .models import (
    Author,
    Category,
    Publisher,
    Book,
)

from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer,
    BookSerializer,
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

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class PublisherDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    -> Retrieve a publisher
    PUT    -> Update a publisher
    PATCH  -> Partially update a publisher
    DELETE -> Delete a publisher
    """

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookListView(generics.ListCreateAPIView):
    """
    GET  -> List books
    POST -> Create a book
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    -> Retrieve a book
    PUT    -> Update a book
    PATCH  -> Partially update a book
    DELETE -> Delete a book
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

class BookSearchView(generics.ListAPIView):
    """
    Search books by title, ISBN, author, or category.
    """

    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get_queryset(self):
        keyword = self.request.query_params.get("keyword", "").strip()

        if not keyword:
            return Book.objects.none()

        return Book.objects.filter(
            Q(title__icontains=keyword)
            | Q(isbn__icontains=keyword)
            | Q(author__name__icontains=keyword)
            | Q(category__name__icontains=keyword)
        )