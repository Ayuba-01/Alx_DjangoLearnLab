from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    GET /api/notifications/ — the current user's notifications.
    Unread first, then newest.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # unread first, then most recent
        return (
            Notification.objects
            .filter(recipient=self.request.user)
            .order_by("is_read", "-timestamp")
            .select_related("actor", "content_type")
        )
