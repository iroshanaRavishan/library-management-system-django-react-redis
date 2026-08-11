from rest_framework import serializers

from .models import Author

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # Serializer for Author model.
