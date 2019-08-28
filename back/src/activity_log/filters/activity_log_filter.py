from django_filters import rest_framework as filters

from activity_log.models import ActivityLog


class ActivityLogFilter(filters.FilterSet):
    activity_from = filters.DateFilter(field_name="date", lookup_expr='gte')
    activity_to = filters.DateFilter(field_name="date", lookup_expr='lte')
    activity = filters.ChoiceFilter(choices=ActivityLog.ACTIVITY_TYPE)

    class Meta:
        model = ActivityLog
        fields = ['activity_from', 'activity_to', 'activity']