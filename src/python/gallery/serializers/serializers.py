from rest_framework import serializers

from gallery.models.album import Album
from gallery.models.category import Category, Tag
from gallery.models.photo import Photo
from gallery.models.user_favorites import AlbumUserFavorites
from gallery.utils import s3_manager


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AlbumUserFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumUserFavorites
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    # read-only serializers
    preview = serializers.StringRelatedField(read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'date', 'folder_path', 'owner', 'preview', 'categories']

    def get_categories(self, obj):
        album_categories = obj.albumcategory_set.select_related('category')
        categories = list()
        return album_categories

    def create(self, validated_data):
        owner = validated_data['current_user']
        album_instance = Album.objects.create(**validated_data, owner=owner)
        return album_instance


class PhotoSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='album.id')
    get_photo_url = serializers.SerializerMethodField()
    get_thumbnail_url = serializers.SerializerMethodField()
    put_photo_url = serializers.SerializerMethodField()
    put_thumbnail_url = serializers.SerializerMethodField()

    def get_get_photo_url(self, obj):
        return s3_manager.get_get_signed_url(obj.album.folder_path + '/' + obj.filename)

    def get_put_photo_url(self, obj):
        return s3_manager.get_put_signed_url(obj.album.folder_path + '/' + obj.filename)

    def get_get_thumbnail_url(self, obj):
        return s3_manager.get_get_signed_url(obj.thumbnail_file)

    def get_put_thumbnail_url(self, obj):
        return s3_manager.get_put_signed_url(obj.thumbnail_file)

    class Meta:
        model = Photo
        fields = ['album_id', 'filename', 'date', 'thumbnail_file', 'get_photo_url', 'put_photo_url',
                  'get_thumbnail_url', 'put_thumbnail_url']
