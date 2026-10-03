from django.urls import path

from borrowing.views import (
    BorrowBookView,
    ReturnBookView,
    MyBorrowingHistoryView,
)


urlpatterns = [

    path(
        "borrow/",
        BorrowBookView.as_view(),
        name="borrow-book",
    ),

    path(
        "return/",
        ReturnBookView.as_view(),
        name="return-book",
    )
]