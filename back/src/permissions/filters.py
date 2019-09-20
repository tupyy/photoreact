from django_filters import rest_framework as filters
from permissions.models import PermissionLog


class PermissionLogFilter(filters.FilterSet):
    log_from = filters.DateFilter(field_name="date", lookup_expr='gte')
    log_to = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = PermissionLog
        fields = ['album_from', 'album_to', 'name']
