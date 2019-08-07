from datetime import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm

from gallery.models.album import Album
from gallery.models.photo import Photo
from gallery.serializers.permission_serializer import ObjectPermissionSerializer


class TestUserObjectSerializer(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')

        today = datetime.today()
        self.album = Album.objects.create(dirpath='foo', date=today, owner=self.user)
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail='thumbnail')

        self.album.save()
        assign_perm("add_photos", self.user, self.album)

    def test_user_object_serializer(self):
        object_permissions = UserObjectPermission.objects.all().select_related("object_pk")
        s = ObjectPermissionSerializer(object_permissions[0])
        print(s.data)