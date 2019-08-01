from django.shortcuts import get_object_or_404
from rest_framework import serializers

from gallery.models import AlbumAccessPolicy, Album
from gallery.serializers.auth_serializer import UserIDSerializer, GroupIDSerializer


class AlbumAccessPolicySerializer(serializers.ModelSerializer):
    users = UserIDSerializer(many=True, read_only=True)
    groups = GroupIDSerializer(many=True, read_only=True)
    album_id = serializers.IntegerField(source='album.id')

    class Meta:
        model = AlbumAccessPolicy
        fields = ['users', 'groups', 'public', 'album_id']

    def create(self, validated_data):
        album = get_object_or_404(Album, pk=validated_data.get('album_id'))
        is_public = bool(validated_data.get('public',False))
        album_access_policy = AlbumAccessPolicy(album=album, public=is_public)

        # add user and groups
        users_ids = validated_data.get('users')
        if not users_ids:
            user_id_serializer = UserIDSerializer()
            for user_id in users_ids:
                album_access_policy.users.add(user_id_serializer.get_object(user_id))

        # add groups
        group_ids = validated_data.get('groups')
        if not group_ids:
            group_id_serializer = GroupIDSerializer()
            for group_id in group_ids:
                album_access_policy.groups.add(group_id_serializer.get_object(group_id))

        album_access_policy.save()
        return album_access_policy


