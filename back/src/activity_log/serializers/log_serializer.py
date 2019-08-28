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
            return self.get_object_data(value)
        else:
            raise Exception("Unexpected type of object")

    def get_object_data(self, obj):
        data = dict()
        data["id"] = obj.id
        data["name"] = obj.name if isinstance(obj, Album) else obj.filename
        data['type'] = "album" if isinstance(obj, Album) else "photo"
        data['link'] = self.get_object_link(obj)
        return data

    def get_object_link(self, obj):
        API_BASE = "/album/" if isinstance(obj, Album) else "/photo/"
        return "{}{}/".format(API_BASE, obj.id)


class ActivityLogSerializer(serializers.ModelSerializer):
    content_object = ObjectRelatedField(read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = ActivityLog
        fields = ['user', 'content_object', 'date', 'activity']
        read_only_fields = ['user', 'content_object', 'date', 'activity']
