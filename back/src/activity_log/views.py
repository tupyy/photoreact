from collections import OrderedDict, Iterable

from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from activity_log.filters import ActivityLogFilter
from activity_log.models import ActivityLog
from activity_log.serializers.log_serializer import ActivityLogSerializer


class StandardActivityLogPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class OrderingMixin(object):

    def get_ordering(self, qs):
        order_fields = self.request.GET.getlist('ordering')
        if len(order_fields) == 0:
            return qs
        for order_field in order_fields:
            if self.is_field(order_field):
                qs = qs.order_by(order_field)
        return qs

    def is_field(self, field_name):
        all_fields = ActivityLog._meta.get_fields()
        return field_name in [field.name for field in all_fields]


class ActivityLogView(OrderingMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    model = ActivityLog
    queryset = ActivityLog.objects

    serializer_class = ActivityLogSerializer
    pagination_class = StandardActivityLogPagination

    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = ActivityLogFilter

    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        If the current user is superuser just call the super
        If not filter the qs with the activities only for the current user
        """
        if not request.user.is_superuser:
            self.queryset = self.queryset.filter(user__id=self.request.user.id)
        self.queryset = self.get_ordering(self.queryset)
        return super().list(request, *args, **kwargs)
# Create your views here.
