from django_filters import rest_framework as filters

from gallery.models.album import Album


class AlbumFilter(filters.FilterSet):
    start = filters.DateFilter(field_name="date", lookup_expr='gte')
    end = filters.DateFilter(field_name="date", lookup_expr='lte')
    name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Album
        fields = ['start', 'end', 'name']
