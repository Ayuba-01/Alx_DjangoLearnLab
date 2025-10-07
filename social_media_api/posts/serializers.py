from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "bio")
        read_only_fields = ("id", "email", "full_name", "bio")


class PostSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    # Optional: convenient count for list views
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "comment_count", "created_at", "updated_at")
        read_only_fields = ("author", "created_at", "updated_at")

    def get_comment_count(self, obj):
        # Use annotated value if present, otherwise count
        return getattr(obj, "comment_count", obj.comments.count())

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "content", "author", "created_at", "updated_at")
        read_only_fields = ("author", "created_at", "updated_at")

    def validate_content(self, value):
        text = (value or "").strip()
        if not text:
            raise serializers.ValidationError("Comment cannot be empty.")
        if len(text) < 2:
            raise serializers.ValidationError("Comment is too short.")
        return text
