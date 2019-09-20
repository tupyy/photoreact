from django_filters import rest_framework as filters
from permissions.models import PermissionLog


class PermissionLogFilter(filters.FilterSet):
    log_from = filters.DateFilter(field_name="date", lookup_expr='gte')
    log_to = filters.DateFilter(field_name="date", lookup_expr='lte')
    name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = PermissionLog
        fields = ['log_from', 'log_to', 'name']
