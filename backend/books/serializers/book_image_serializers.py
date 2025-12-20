from books.models import BookImage
from rest_framework import serializers


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ["id", "image", "description"]
