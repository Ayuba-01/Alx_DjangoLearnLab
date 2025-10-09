from django.contrib.contenttypes.models import ContentType
from .models import Notification

def notify(*, recipient, actor, verb: str, target=None):
    """
    Create a Notification. 'target' can be any model instance (Post, Comment, User, ...).
    """
    content_type = object_id = None
    if target is not None:
        ct = ContentType.objects.get_for_model(target.__class__)
        content_type, object_id = ct, target.pk
    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id,
    )
