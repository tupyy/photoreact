from django.contrib.auth.models import User, Group
from rest_framework import serializers

from permissions.models import PermissionLog


class ObjectRelatedField(serializers.RelatedField):
    """
    Custom field for content_object in PermissionLog model
    """

    def to_representation(self, value):
        if isinstance(value, User) or isinstance(value, Group):
            return self.get_object_data(value)
        raise Exception("Unexpected type of object")

    def get_object_data(self, value):
        data = dict()
        data['id'] = value.id
        data['name'] = str(value)
        data['type'] = 'user' if isinstance(value,User) else 'group'
        return data


class PermissionLogSerializer(serializers.ModelSerializer):
    content_object = ObjectRelatedField(read_only=True)
    user_from = serializers.CharField(source='user_from.username')

    class Meta:
        model = PermissionLog
        fields = ['user_from', 'content_object','date', 'permission', 'action']
        read_only_fields = ['user_from', 'content_object','date', 'permission', 'action']