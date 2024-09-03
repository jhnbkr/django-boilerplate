from typing import Any, Generic, List, TypeVar
from urllib.parse import urlencode

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest
from ninja import Field, Schema
from ninja.pagination import PaginationBase

T = TypeVar("T")


class StaticListSchema(Schema, Generic[T]):
    items: List[T]
    total: int


class LimitOffsetPagination(PaginationBase, Generic[T]):
    class Input(Schema):
        limit: int = Field(settings.PAGINATION_DEFAULT_PAGE_LIMIT, ge=1)
        offset: int = Field(0, ge=0)

    class Output(Schema):
        items: List[T]
        limit: int
        offset: int
        total: int
        next: str | None
        previous: str | None

    items_attribute: str = "items"

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        request: HttpRequest,
        **params: Any,
    ) -> Output:
        offset = pagination.offset
        limit = min(pagination.limit, settings.PAGINATION_MAX_PAGE_LIMIT)

        items = list(queryset[offset : offset + limit])
        total = self._items_count(queryset)

        base_url = request.build_absolute_uri(request.path)
        next_offset = offset + limit if offset + limit < total else None
        previous_offset = max(offset - limit, 0) if offset > 0 else None

        next_url = (
            self._build_pagination_url(base_url, next_offset, limit)
            if next_offset is not None
            else None
        )
        previous_url = (
            self._build_pagination_url(base_url, previous_offset, limit)
            if previous_offset is not None
            else None
        )

        return {
            "items": items,
            "limit": limit,
            "offset": offset,
            "total": total,
            "next": next_url,
            "previous": previous_url,
        }

    def _build_pagination_url(self, base_url: str, offset: int, limit: int) -> str:
        params = {"offset": offset, "limit": limit}
        return f"{base_url}?{urlencode(params)}"
