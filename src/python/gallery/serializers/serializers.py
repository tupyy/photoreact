from rest_framework import serializers

from gallery.models import Album, Photo, Category, Tag
from gallery.utils.s3_manager import get_signed_url, put_signed_url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    preview = serializers.StringRelatedField()

    class Meta:
        model = Album
        fields = ['id', 'name', 'categories', 'tags', 'owner', 'preview']


class PhotoSerializer(serializers.ModelSerializer):
    get_photo_url = serializers.SerializerMethodField(source='get_photo_signed_url')
    get_thumbnail_url = serializers.SerializerMethodField(source='get_thumbnail_signed_url')
    put_photo_url = serializers.SerializerMethodField(source='put_photo_signed_url')
    put_thumbnail_url = serializers.SerializerMethodField(source='put_thumbnail_signed_url')

    def get_photo_signed_url(self):
        return get_signed_url(self.album.dirpath + '/' + self.filename)

    def put_photo_signed_url(self):
        return put_signed_url(self.album.dirpath + '/' + self.filename)

    def get_thumbnail_signed_url(self):
        return get_signed_url(self.thumbnail)

    def put_thumbnail_signed_url(self):
        return put_signed_url(self.thumbnail)

    class Meta:
        model = Photo
        fields = ['__all__', 'get_photo_url', 'put_photo_url', 'get_thumbnail_url', 'put_thumbnail_url']
