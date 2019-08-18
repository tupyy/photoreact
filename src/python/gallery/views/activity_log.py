from collections import OrderedDict

from django_filters import rest_framework as filters
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.filters.activity_log_filter import ActivityLogFilter
from gallery.models.album import ActivityLog
from gallery.serializers.log_serializer import ActivityLogSerializer


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


class ActivityLogView(mixins.ListModelMixin,
                      GenericViewSet):
    model = ActivityLog
    queryset = ActivityLog.objects

    serializer_class = ActivityLogSerializer
    pagination_class = StandardActivityLogPagination

    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = ActivityLogFilter

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        If the current user is superuser just call the super
        If not filter the qs with the activities only for the current user
        """
        if not request.user.is_superuser:
            self.queryset = self.queryset.filter(user__id=self.request.user.id)
        self.queryset = self.queryset.order_by('-date')
        return super().list(request, *args, **kwargs)
