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
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    dirpath = serializers.CharField()
    date = serializers.DateField()
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    preview = serializers.StringRelatedField()

    class Meta:
        model = Album
        fields = ['id', 'name', 'categories', 'date', 'dirpath', 'tags', 'owner', 'preview']

    def validate(self, data):
        return data

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        categories_data = validated_data.pop('categories')
        tags_data = validated_data.pop('tags')

        album_instance = Album.objects.create(**validated_data, owner=owner)
        for category in self._get_objects(Category, categories_data):
            album_instance.categories.add(category)

        for tag in self._get_objects(Tag, tags_data):
            album_instance.tags.add(tag)

        return album_instance

    def update(self, instance, validated_data):
        """ Don't allow dirpath update"""
        instance.name = validated_data.pop('name')
        instance.date = validated_data.pop('date')

        categories = self._get_objects(Category,validated_data.pop('categories'))
        for category in categories:
            if category not in instance.categories.all():
                instance.categories.add(category)

        tags = self._get_objects(Tag, validated_data.pop('tags'))
        for tag in tags:
            if tag not in instance.tags.all():
                instance.tags.add(tag)
        return instance

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
