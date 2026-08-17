from django.shortcuts import render

from rest_framework import generics

from .models import (Author)

from .serializers import (AuthorSerializer)

from .permissions import IsLibrarianOrReadOnly


class AuthorListView(generics.ListCreateAPIView):
    """
    GET  -> List authors
    POST -> Create an author
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

