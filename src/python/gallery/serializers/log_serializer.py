from rest_framework import serializers

from gallery.models.album import Album
from gallery.models.album import ActivityLog
from gallery.models.photo import Photo
from gallery.serializers.serializers import AlbumSerializer, PhotoSerializer


class ObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for content_object in ActivityLog
    """

    def to_representation(self, value):
        if isinstance(value, Album):
            serializer = AlbumSerializer(value)
        elif isinstance(value, Photo):
            serializer = PhotoSerializer(value)
        else:
            raise Exception("Unexpected type of object")
        return serializer


class ActivityLogSerializer(serializers.ModelSerializer):
    content_object = ObjectRelatedField(read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = ActivityLog
        fields = ['user', 'content_object', 'date', 'activity']
