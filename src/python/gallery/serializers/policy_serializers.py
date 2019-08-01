from rest_framework import serializers

from gallery.models import AlbumAccessPolicy
from gallery.serializers.auth_serializer import UserSerializer, GroupSerializer


class AlbumAccessPolicySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    album_id = serializers.IntegerField(source='album.id')

    class Meta:
        model = AlbumAccessPolicy
        fields = ['users', 'groups', 'public', 'album_id']
