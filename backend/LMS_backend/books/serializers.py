from rest_framework import serializers

from .models import Author, Category, Publisher, Book

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # Serializer for Author model.

    class Meta:
        model = Author

        fields = [
            "url",
            "id",
            "name",
            "biography",
        ]

        extra_kwargs = {
            "url": {
                "view_name": "author-detail"
            }
        }



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # Serializer for Category model.

    class Meta:
        model = Category

        fields = [
            "url",
            "id",
            "name",
            "description",
        ]

        extra_kwargs = {
            "url": {
                "view_name": "category-detail"
            }
        }


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    # Serializer for Publisher model.

    class Meta:
        model = Publisher

        fields = [
            "url",
            "id",
            "name",
            "address",
        ]

        extra_kwargs = {
            "url": {
                "view_name": "publisher-detail"
            }
        }



class BookSerializer(serializers.HyperlinkedModelSerializer):
    # Serializer for Book model.
    author = serializers.HyperlinkedRelatedField(
        view_name="author-detail",
        queryset=Author.objects.all(),
    )
