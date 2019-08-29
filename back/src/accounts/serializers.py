from rest_framework import serializers

from accounts.models import UserProfile
from gallery.utils import s3_manager


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    photo = serializers.SerializerMethodField()
    roles = serializers.SlugRelatedField(read_only=True, many=True, slug_field="id")

    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name",
                  "last_name", "email", "photo", "roles"]

    def get_photo(self, obj):
        from photogallery.settings import STATIC_PROFILE_PHOTO_URL
        return s3_manager.get_get_signed_url(STATIC_PROFILE_PHOTO_URL + obj.photo_filename)
