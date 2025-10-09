from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Notification

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name")
        read_only_fields = fields

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserMiniSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "id", "verb", "is_read", "timestamp",
            "actor", "target_type", "target_id", "target_repr",
        )
        read_only_fields = fields

    def get_target_type(self, obj):
        return obj.content_type.model if obj.content_type else None

    def get_target_id(self, obj):
        return obj.object_id

    def get_target_repr(self, obj):
        return str(obj.target) if obj.target else None
