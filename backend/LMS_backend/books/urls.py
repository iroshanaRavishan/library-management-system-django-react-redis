from django.urls import path

from .views import (AuthorListView)


urlpatterns = [

    # Authors
    path(
        "authors/",
        AuthorListView.as_view(),
        name="author-list",
    ),
]