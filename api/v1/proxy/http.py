from datetime import datetime
from uuid import UUID

import requests
from ninja import Router, Schema

from proxy.models import HttpMethod, HttpRequest, HttpResponse

router = Router()


class HttpResponseSchema(Schema):
    id: UUID
    status_code: int
    headers: dict[str, str] | None = None
    content: str | None = None
    metadata: dict | None = None
    created_at: datetime


class HttpRequestSchema(Schema):
    id: UUID
    method: HttpMethod
    url: str
    headers: dict[str, str] | None = None
    params: dict[str, str] | None = None
    body: dict | None = None
    metadata: dict | None = None
    created_at: datetime


class ProxyHttpRequestInput(Schema):
    method: HttpMethod
    url: str
    headers: dict[str, str] | None = None
    params: dict[str, str] | None = None
    body: dict | None = None


class ProxyHttpRequestResponse(Schema):
    request: HttpRequestSchema
    response: HttpResponseSchema


@router.post(
    "/request",
    url_name="proxy-http-request",
    response=ProxyHttpRequestResponse,
)
def proxy_http_request(request, data: ProxyHttpRequestInput):
    request_instance = HttpRequest.objects.create(
        method=data.method,
        url=data.url,
        headers=data.headers,
        params=data.params,
        body=data.body,
    )

    response = requests.request(
        method=request_instance.method,
        url=request_instance.url,
        headers=request_instance.headers,
        params=request_instance.params,
        json=request_instance.body,
    )

    response_instance = HttpResponse.objects.create(
        request=request_instance,
        status_code=response.status_code,
        headers=dict(response.headers),
        content=response.text,
    )

    return {
        "request": {
            "id": request_instance.id,
            "method": request_instance.method,
            "url": request_instance.url,
            "headers": request_instance.headers,
            "params": request_instance.params,
            "body": request_instance.body,
            "metadata": request_instance.metadata,
            "created_at": request_instance.created_at,
        },
        "response": {
            "id": response_instance.id,
            "status_code": response_instance.status_code,
            "headers": response_instance.headers,
            "content": response_instance.content,
            "metadata": response_instance.metadata,
            "created_at": response_instance.created_at,
        },
    }
