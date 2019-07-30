from rest_framework import serializers

from gallery.models import Album, Photo, Category, Tag


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
    get_url = serializers.ReadOnlyField(source='get_signed_url')
    put_url = serializers.ReadOnlyField(source='put_signed_url')

    class Meta:
        model = Photo
        fields = ['__all__', 'get_url', 'put_url']
