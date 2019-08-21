from django_filters import rest_framework as filters

from gallery.models.activity_log import ActivityLog


class ActivityLogFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = ActivityLog
        fields = ['start_date', 'end_date']