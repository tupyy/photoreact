from guardian.models import UserObjectPermission
from rest_framework import serializers

from gallery.serializers.auth_serializer import UserSerializer
from gallery.serializers.serializers import AlbumSerializer


class ObjectPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    album = AlbumSerializer()

    user_id = serializers.IntegerField(source='user.id',
                                       write_only=True)

    class Meta:
        model = UserObjectPermission
        fields = ['user', 'user_id', "album"]
