import uuid

from django.db import models
from django.utils import timezone

DEFAULT_ORDERING = ["-created_at"]
DEFAULT_VARCHAR_LENGTH = 255


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = DEFAULT_ORDERING
