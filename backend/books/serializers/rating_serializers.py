from books.models import Rating
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ("id", "user", "book", "score")
        read_only_fields = ("id", "user", "book")

    # @ Prevent user from rating the same book more than once
    def validate(self, attrs):
        request = self.context["request"]
        view = self.context["view"]

        if view.action == "create":
            user = request.user
            book_id = view.kwargs["book_pk"]

            if Rating.objects.filter(user=user, book_id=book_id).exists():
                raise serializers.ValidationError({"detail": "You have already rated this book."})

        return attrs
