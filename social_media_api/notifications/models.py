from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    recipient <-- actor did <verb> on target
    target is generic so this works for follows, likes, comments, etc.
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    verb = models.CharField(max_length=50)  # e.g. "followed", "liked", "commented"

    # Generic target (optional for some verbs like "followed")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    target = GenericForeignKey("content_type", "object_id")

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["recipient", "is_read", "-timestamp"]),
        ]

    def __str__(self) -> str:
        tgt = f" {self.target}" if self.target else ""
        return f"To {self.recipient}: {self.actor} {self.verb}{tgt} @ {self.timestamp:%Y-%m-%d %H:%M}"
