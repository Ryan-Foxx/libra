from books.models import Favorite
from rest_framework import serializers


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "book", "datetime_created"]
        read_only_fields = ["id", "datetime_created"]
