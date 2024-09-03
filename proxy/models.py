from django.db import models

from common.models.base import BaseModel


class HttpMethod(models.TextChoices):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpRequestManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("response")


class HttpRequest(BaseModel):
    method = models.CharField(choices=HttpMethod.choices, max_length=16)
    url = models.CharField(max_length=2048)
    headers = models.JSONField(blank=True, null=True)
    params = models.JSONField(blank=True, null=True)
    body = models.JSONField(blank=True, null=True)

    objects = HttpRequestManager()


class HttpResponse(BaseModel):
    request = models.OneToOneField(
        HttpRequest,
        on_delete=models.CASCADE,
        related_name="response",
    )
    status_code = models.IntegerField()
    headers = models.JSONField(blank=True, null=True)
    content = models.TextField(blank=True)
