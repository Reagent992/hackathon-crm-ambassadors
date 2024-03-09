from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import decorators, mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ambassadors.models import Promo
from api.v1.serializers.promos_serializer import PromoSerializer
from core.choices import PromoStatus


@extend_schema(tags=["Промокоды"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список промокодов амбассадоров."),
        description=(
            "<ul><h3>Фильтрация:</h3>"
            "<li>Фильтрация по дате: <code>./?created_after=2023-04-25"
            "&created_before=2024-03-25</code>    "
            "т.е. дата старше 2023-04-25 и младше 2024-03-25</li>"
            "<li>Фильтрация по статусу амбассадора: "
            "<code>./?ambassador__status=active</code> "
            "т.е. active(активный)/paused(на паузе)/"
            "not_ambassador(не амбассадор)/pending(уточняется)</li>"
            "<h3>Поиск:</h3>"
            "<li>Поиск по имени: <code>./?search=Вася</code></li>"
            "</ul>"
        ),
    ),
    retrieve=extend_schema(summary="Активный промокод амбассадора."),
    partial_update=extend_schema(
        summary="Редактирование промокода амбассадора.",
    ),
    archive=extend_schema(summary="Список архивных промокодов"),
)
class PromosViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    """
    Промокоды амбассадоров.
    Фильтрация по статусу амбассадора (/?ambassador__status=active).
    Фильтр по дате (/?created_after=2024-02-23&created_before=2024-02-26).
    Поиск по имени (/?search=Смирнова).
    Сортировка по дате (/?ordering=-ambassador__created).
    """

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("ambassador__status",)
    search_fields = ("ambassador__name",)
    ordering_fields = ("ambassador__created",)
    ordering = ("ambassador__created",)
    http_method_names = ("get", "head", "options", "patch")
    serializer_class = PromoSerializer

    def get_queryset(self):
        queryset = Promo.objects.filter(status=PromoStatus.ACTIVE)
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        if created_after:
            queryset = queryset.filter(ambassador__created__gte=created_after)
        if created_before:
            queryset = queryset.filter(ambassador__created__lte=created_before)
        return queryset

    @extend_schema(summary="Архивные промокоды амбассадоров")
    @decorators.action(
        methods=("get",),
        detail=False,
        url_path="archive",
    )
    def get_archive_promos(self, request):
        """Архивные промокоды амбассадоров."""

        queryset = Promo.objects.filter(status=PromoStatus.ARCHIVED)
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        ambassador__status = self.request.query_params.get(
            "ambassador__status"
        )
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get(
            "ordering", "ambassador__created"
        )
        if search:
            queryset = queryset.filter(ambassador__name__icontains=f"{search}")
        if ambassador__status:
            queryset = queryset.filter(ambassador__status=ambassador__status)
        if created_after:
            queryset = queryset.filter(ambassador__created__gte=created_after)
        if created_before:
            queryset = queryset.filter(ambassador__created__lte=created_before)
        if ordering:
            queryset = queryset.order_by(f"{ordering}")
        page = self.paginate_queryset(queryset)
        serializer = PromoSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
