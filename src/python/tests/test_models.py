from django.contrib.auth.models import Group, User
from django.test import TestCase
import datetime

from gallery.models import Album, Photo, Tag
from gallery.models import Category
from gallery.serializers.serializers import AlbumSerializer


class AlbumTests(TestCase):

    def setUp(self) -> None:
        today = datetime.date.today()
        self.album = Album.objects.create(dirpath='foo', date=today)
        self.photo = Photo.objects.create(album=self.album, filename='bar')
        self.category = Category.objects.create(name="categorie")

        self.album.save()
        self.album.categories.add(self.category)

        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')

    def test_category(self):
        self.assertEqual(self.album.categories.all().count(), 1)

    def test_album_serializer(self):
        self.album.tags.add(Tag.objects.create(name="my tag"))
        albumS = AlbumSerializer(self.album)
        print(albumS.data)
        self.assertTrue(True)


