from django.urls import path

from .views import (
    AuthorListView,
    AuthorDetailView,
    CategoryListView,
    CategoryDetailView,
    PublisherListView,
    PublisherDetailView,
    BookListView,
    BookDetailView,
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
        "books/<int:pk>/",
        BookDetailView.as_view(),
        name="book-detail",
    ),
]