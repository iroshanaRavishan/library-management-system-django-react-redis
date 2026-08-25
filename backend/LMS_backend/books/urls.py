from django.urls import path

from .views import (
    AuthorListView,
    AuthorDetailView,
    CategoryListView,
    CategoryDetailView
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
]