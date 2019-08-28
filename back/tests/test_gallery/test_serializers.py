from datetime import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase

from gallery.models.album import Album
from gallery.models.category import Category
from gallery.models.photo import Photo
from gallery.serializers.serializers import AlbumSerializer, PhotoSerializer


class TestAlbumSerializer(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.today()
        self.album = Album.objects.create(folder_path='foo', date=today.date(), owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail')

        self.category = Category.objects.create(name="foo")
        self.category.save()
        self.category2 = Category.objects.create(name="bar")
        self.category2.save()

        self.album.save()
        self.album.categories.add(self.category, self.category2)

    def test_serialize_fields(self):
        s = AlbumSerializer(self.album)
        self.assertEqual("user", s.data['owner'])
        self.assertFalse(s.data['preview'] is None)
        self.assertTrue(self.user.has_perm('add_photos', self.album))
        self.assertTrue(self.user.has_perm('change_album', self.album))
        self.assertTrue(self.user.has_perm('delete_album', self.album))
        self.assertTrue(self.user.has_perm('add_permissions', self.album))
        self.assertTrue(self.user.has_perm('change_permissions', self.album))
        self.assertTrue(self.user.has_perm('delete_permissions', self.album))

    def test_photo_serializer(self):
        p = PhotoSerializer(self.photo)
        self.assertFalse(p.data['get_photo_url'] is None)
        self.assertFalse(p.data['get_thumbnail_url'] is None)
