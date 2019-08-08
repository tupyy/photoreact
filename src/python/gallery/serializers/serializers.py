from guardian.shortcuts import assign_perm
from rest_framework import serializers

from gallery.models.album import Album
from gallery.models.photo import Photo
from gallery.models.category import Category, Tag
from gallery.utils.s3_manager import get_get_signed_url, get_put_signed_url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    dirpath = serializers.CharField()
    date = serializers.DateField()
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    preview = serializers.StringRelatedField()

    class Meta:
        model = Album
        fields = ['id', 'name', 'date', 'dirpath', 'owner', 'preview']

    def validate(self, data):
        return data

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        album_instance = Album.objects.create(**validated_data, owner=owner)

        # Assign all permissions to user
        assign_perm('add_photos', owner, album_instance)
        assign_perm('change_album', owner, album_instance)
        assign_perm('delete_album', owner, album_instance)
        assign_perm('add_permissions', owner, album_instance)
        assign_perm('change_permissions', owner, album_instance)
        assign_perm('delete_permissions', owner, album_instance)

        return album_instance

    def _get_objects(self, model, data):
        """ Get categories or tags """
        objects = [model.objects.get_or_create(name=entry.get('name'))[0]
                   for entry in data]
        return objects


class PhotoSerializer(serializers.ModelSerializer):
    get_photo_url = serializers.SerializerMethodField(source='get_photo_signed_url')
    get_thumbnail_url = serializers.SerializerMethodField(source='get_thumbnail_signed_url')
    put_photo_url = serializers.SerializerMethodField(source='put_photo_signed_url')
    put_thumbnail_url = serializers.SerializerMethodField(source='put_thumbnail_signed_url')

    def get_photo_signed_url(self):
        return get_get_signed_url(self.album.dirpath + '/' + self.filename)

    def put_photo_signed_url(self):
        return get_put_signed_url(self.album.dirpath + '/' + self.filename)

    def get_thumbnail_signed_url(self):
        return get_get_signed_url(self.thumbnail)

    def put_thumbnail_signed_url(self):
        return get_put_signed_url(self.thumbnail)

    class Meta:
        model = Photo
        fields = ['__all__', 'get_photo_url', 'put_photo_url', 'get_thumbnail_url', 'put_thumbnail_url']
