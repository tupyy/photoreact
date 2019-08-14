from django.contrib.auth.models import User
from rest_framework import serializers

from gallery.models.album import Album
from gallery.models.category import Category, Tag
from gallery.models.photo import Photo
from gallery.models.user_favorites import AlbumUserFavorites
from gallery.utils import s3_manager


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ['id', 'name']


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
    categories = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")
    tags = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")
    favorites = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")

    class Meta:
        model = Album
        fields = ['id', 'name', 'date', 'description',
                  'folder_path', 'owner', 'preview',
                  'categories', 'tags', 'favorites']

    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        owner = User.objects.filter(username__exact=owner_data['username']).first()
        album_instance = Album.objects.create(**validated_data, owner=owner)
        return album_instance


class PhotoSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='album.id')
    get_photo_url = serializers.SerializerMethodField()
    get_thumbnail_url = serializers.SerializerMethodField()

    def get_get_photo_url(self, obj):
        """
        Return the GET signed URL for photo
        :param obj:
        :return: S3 signed URL for GET method
        """
        return s3_manager.get_get_signed_url(obj.album.folder_path + '/' + obj.filename)

    def get_get_thumbnail_url(self, obj):
        """
        Return GET signed URL for thumbnail
        :param obj:
        :return: S3 signed URL for GET method
        """
        return s3_manager.get_get_signed_url(obj.thumbnail_file)

    class Meta:
        model = Photo
        fields = ['id', 'album_id', 'filename', 'date', 'thumbnail_file',
                  'get_photo_url', 'get_thumbnail_url']
