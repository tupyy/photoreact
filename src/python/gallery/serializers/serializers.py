from rest_framework import serializers

from src.python.gallery.models import Album, Photo


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['__all__']


class PhotoSerializer(serializers.ModelSerializer):
    get_url = serializers.ReadOnlyField(source='get_signed_url')
    put_url = serializers.ReadOnlyField(source='put_signed_url')

    class Meta:
        model = Photo
        fields = ['__all__', 'get_url', 'put_url']
