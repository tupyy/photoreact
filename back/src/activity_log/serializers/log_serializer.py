from rest_framework import serializers

from gallery.models.album import Album
from activity_log.models import ActivityLog
from gallery.models.photo import Photo


class ObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for content_object in ActivityLog
    """

    def to_representation(self, value):
        if isinstance(value, Album) or isinstance(value, Photo):
            return value.id
        else:
            raise Exception("Unexpected type of object")


class ActivityLogSerializer(serializers.ModelSerializer):
    content_object = ObjectRelatedField(read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = ActivityLog
        fields = ['user', 'content_object', 'date', 'activity']
        read_only_fields = ['user', 'content_object', 'date', 'activity']
