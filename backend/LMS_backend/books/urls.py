from django.urls import path

from books.views import (
    AuthorListView,
    AuthorDetailView,
    CategoryListView,
    CategoryDetailView,
    PublisherListView,
    PublisherDetailView,
    BookListView,
    BookDetailView,
    BookSearchView,
    PopularBooksView,
    CategoryBooksView,
)


urlpatterns = [

    # Authors
    path(
        "authors/",
        AuthorListView.as_view(),
        name="author-list",
    ),

    path(
        "authors/<int:pk>/",
        AuthorDetailView.as_view(),
        name="author-detail",
    ),

    # Categories
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list",
    ),

    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),

    path(
        "categories/<int:category_id>/books/",
        CategoryBooksView.as_view(),
        name="category-books",
    ),

    # Publishers
    path(
        "publishers/",
        PublisherListView.as_view(),
        name="publisher-list",
    ),

    path(
        "publishers/<int:pk>/",
        PublisherDetailView.as_view(),
        name="publisher-detail",
    ),

    # Books
    path(
        "books/",
        BookListView.as_view(),
        name="book-list",
    ),

    path(
        "books/search/",
        BookSearchView.as_view(),
        name="book-search",
    ),

    path(
        "books/popular/",
        PopularBooksView.as_view(),
        name="popular-books",
    ),

    path(
        "books/<int:pk>/",
        BookDetailView.as_view(),
        name="book-detail",
    ),
]