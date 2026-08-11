from rest_framework import serializers

from .models import Author

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # Serializer for Author model.

    class Meta:
        model = Author

        fields = [
            "url",
            "id",
            "name",
            "biography",
        extra_kwargs = {
            "url": {
                "view_name": "author-detail"
            }
        }
        ]

