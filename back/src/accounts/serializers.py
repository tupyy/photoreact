from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import UserProfile, Role
from gallery.utils import s3_manager


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id", read_only=True)
    active = serializers.BooleanField(source="user.is_active", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    langKey = serializers.CharField(source="lang_key")
    photo = serializers.SerializerMethodField()
    roles = serializers.SlugRelatedField(read_only=True, many=True, slug_field="role")

    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name", "langKey", "active",
                  "last_name", "email", "photo", "roles"]

    def get_photo(self, obj):
        from photogallery.settings import STATIC_PROFILE_PHOTO_URL
        return s3_manager.get_get_signed_url(STATIC_PROFILE_PHOTO_URL + obj.photo_filename)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        first_name = user_data.pop('first_name')
        last_name = user_data.pop('last_name')
        email = user_data.pop('email')
        user = get_object_or_404(User, pk=instance.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return instance
