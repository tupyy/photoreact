from django_filters import rest_framework as filters
from gallery.models.album import Album


class AlbumFilter(filters.FilterSet):
    album_from = filters.DateFilter(field_name="date", lookup_expr='gte')
    album_to = filters.DateFilter(field_name="date", lookup_expr='lte')
    name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Album
        fields = ['album_from', 'album_to', 'name']
