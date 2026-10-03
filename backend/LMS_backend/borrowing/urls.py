from django.urls import path

from borrowing.views import (
    BorrowBookView,
    ReturnBookView,
    MyBorrowingHistoryView,
    BorrowingListView,
    BorrowingDetailView,
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
    ),

    path(
        "my-history/",
        MyBorrowingHistoryView.as_view(),
        name="my-borrowing-history",
    ),

    path(
        "<int:pk>/",
        BorrowingDetailView.as_view(),
        name="borrowing-detail",
    ),
]