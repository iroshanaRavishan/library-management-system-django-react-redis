from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response

from .models import (
    Author,
    Category,
    Publisher,
    Book,
)

from .cache import (
    invalidate_book_search_cache,
    invalidate_book_detail_cache,
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


    def perform_create(self, serializer):
    # create a new book and invalidate the cache for book search results

        # save the new book to the database
        serializer.save()

        # invalidate the cache for book search results
        invalidate_book_search_cache()

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

    def retrieve(self, request, *args, **kwargs):

        # Get the book ID from the URL.
        book_id = kwargs["pk"]

        # Redis key for this specific book.
        cache_key = f"book:{book_id}"

        # Try to get the book from Redis.
        cached_data = cache.get(cache_key)

        # Cache HIT
        if cached_data is not None:
            return Response(cached_data)

        # Cache MISS
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        # Store the serialized book in Redis for 30 minutes.
        cache.set(cache_key)

        

class BookSearchView(generics.ListAPIView):
    """
    Search books by title, ISBN, author, or category.
    Results are cached in Redis for 10 minutes.
    """

    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get(self, request, *args, **kwargs):

        # Get search keyword from query parameter
        keyword = request.query_params.get("keyword", "").strip().lower()

        # If no keyword was provided
        if not keyword:
            return Response([])

        # Create a unique Redis key for this search
        cache_key = f"book_search:{keyword}"

        # Try to get results from Redis
        cached_data = cache.get(cache_key)

        # Cache HIT
        if cached_data is not None:
            return Response(cached_data)

        # Cache MISS
        queryset = Book.objects.filter(
            Q(title__icontains=keyword)
            | Q(isbn__icontains=keyword)
            | Q(author__name__icontains=keyword)
            | Q(category__name__icontains=keyword)
        ).distinct()

        # Serialize database results
        serializer = self.get_serializer(
            queryset,
            many=True
        )

        # Store results in Redis for 10 minutes
        cache.set(
            cache_key,
            serializer.data,
            timeout=60 * 10
        )

        return Response(serializer.data)
