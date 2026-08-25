from django.urls import path

from .views import (
    AuthorListView,
    AuthorDetailView
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

]