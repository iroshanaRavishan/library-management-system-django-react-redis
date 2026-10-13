from django.shortcuts import render
from django.db.models import Q, Count
from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response

from .models import (
    Author,
    Category,
    Publisher,
    Book,
)

from books.cache import (
    invalidate_book_search_cache,
    invalidate_book_detail_cache,
    invalidate_category_cache,
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
        # Save the new book.
        book = serializer.save()

        # Clear book search caches.
        invalidate_book_search_cache()

        # Clear the cache for this book's category.
        invalidate_category_cache(book.category_id)

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
        cache.set(
            cache_key,
            serializer.data,
            timeout=60 * 30
        )

        return Response(serializer.data)

    def perform_update(self, serializer):

        # Get the existing book before updating it.
        old_category_id = self.get_object().category_id

        # Save the updated book.
        instance = serializer.save()

        # Invalidate the individual book cache.
        invalidate_book_detail_cache(instance.id)

        # Invalidate search results.
        invalidate_book_search_cache()

        # Invalidate the old category cache.
        invalidate_category_cache(old_category_id)

        # Invalidate the new category cache.
        invalidate_category_cache(instance.category_id)



    def perform_destroy(self, instance):

        # Remember the category before deleting the book.
        category_id = instance.category_id

        # Remember the book ID.
        book_id = instance.id

        # Delete the book.
        instance.delete()

        # Invalidate book detail cache.
        invalidate_book_detail_cache(book_id)

        # Invalidate search caches.
        invalidate_book_search_cache()

        # Invalidate category cache.
        invalidate_category_cache(category_id)

        

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


class PopularBooksView(generics.ListAPIView):
    """
    Returns the most borrowed books.
    Results are cached in Redis.
    """

    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get(self, request, *args, **kwargs):

        # Redis key for popular books.
        cache_key = "popular_books"

        # Check Redis first.
        cached_data = cache.get(cache_key)

        # If data exists in Redis, return it immediately.
        if cached_data is not None:
            return Response(cached_data)

        # Calculate the most borrowed books from the database.
        queryset = (
            Book.objects
            .annotate(
                borrow_count=Count("borrow_transactions")
            )
            .order_by("-borrow_count", "title")[:10]
        )

        # Serialize the books.
        serializer = self.get_serializer(
            queryset,
            many=True
        )

        # Store the result in Redis for 30 minutes.
        cache.set(
            cache_key,
            serializer.data,
            timeout=60 * 30
        )

        # Return the result.
        return Response(serializer.data)



class CategoryBooksView(generics.ListAPIView):
    """
    Returns all books belonging to a specific category.
    Results are cached in Redis.
    """

    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get(self, request, category_id, *args, **kwargs):

        # Create a unique Redis key for this category.
        cache_key = f"category:{category_id}"

        # Check Redis first.
        cached_data = cache.get(cache_key)
