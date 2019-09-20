from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from gallery.serializers.serializers import AlbumSerializer
from permissions.models import PermissionLog


class ObjectRelatedField(serializers.RelatedField):
    """
    Custom field for content_object in PermissionLog model
    """

    def to_representation(self, value):
        if isinstance(value, User):
            return self.get_user_data(value)
        elif isinstance(value, Group):
            return self.get_group_data(value)
        raise Exception("Unexpected type of object")

    def get_common_data(self, value):
        data = dict()
        data['id'] = value.id
        data['type'] = 'user' if isinstance(value, User) else 'group'
        return data

    def get_group_data(self, value):
        data = self.get_common_data(value)
        data['name'] = str(value)
        return data

    def get_user_data(self, value):
        data = self.get_common_data(value)
        user_profile = UserProfile.objects.filter(user__username__exact=value.username).first()
        if user_profile is not None:
            data['profile'] = UserProfileSerializer(user_profile).data
        return data


class PermissionLogSerializer(serializers.ModelSerializer):
    content_object = ObjectRelatedField(read_only=True)
    user_from = serializers.CharField(source='user_from.username')
    permission = serializers.StringRelatedField(source='permission.codename')
    album = AlbumSerializer()

    class Meta:
        model = PermissionLog
        fields = ['user_from', 'content_object', 'date', 'permission', 'album', 'operation']
        read_only_fields = ['user_from', 'content_object', 'date', 'permission', 'album', 'operation']
