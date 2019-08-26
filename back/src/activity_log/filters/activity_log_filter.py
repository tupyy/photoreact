from django_filters import rest_framework as filters

from activity_log.models import ActivityLog


class ActivityLogFilter(filters.FilterSet):
    start = filters.DateFilter(field_name="date", lookup_expr='gte')
    end = filters.DateFilter(field_name="date", lookup_expr='lte')
    activity = filters.ChoiceFilter(choices=ActivityLog.ACTIVITY_TYPE)

    class Meta:
        model = ActivityLog
        fields = ['start', 'end', 'activity']