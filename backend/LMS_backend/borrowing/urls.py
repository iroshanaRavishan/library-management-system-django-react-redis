from django.urls import path

from borrowing.views import (
    BorrowBookView,
    ReturnBookView
)


urlpatterns = [

    path(
        "borrow/",
        BorrowBookView.as_view(),
        name="borrow-book",
    )
]