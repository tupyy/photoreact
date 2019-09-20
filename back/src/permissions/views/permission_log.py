from django_filters import filters
from guardian.mixins import PermissionListMixin
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from permissions.filters import PermissionLogFilter
from permissions.models import PermissionLog
from permissions.serializers import PermissionLogSerializer


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
        all_fields = PermissionLog._meta.get_fields()
        return field_name in [field.name for field in all_fields]


class PermissionLogListView(OrderingMixin,
                            ListAPIView,
                            GenericViewSet):
    queryset = PermissionLog.objects
    serializer_class = PermissionLogSerializer
    lookup_field = 'id'

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PermissionLogFilter

    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = self.get_ordering(self.filter_queryset(self.get_queryset()))
        qs = qs.filter(user_from__username__exact=request.user.username)
        limit = self.request.query_params.get('limit', None)
        try:
            if limit is not None:
                qs = qs.all()[:int(limit)]
        except ValueError:
            pass

        serializer = self.get_serializer(qs, many=True)
        data = dict()
        data['size'] = qs.count()
        data['logs'] = serializer.data
        return Response(data)
