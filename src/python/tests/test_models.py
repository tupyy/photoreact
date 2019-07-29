import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase

from gallery.models import Album, Photo
from gallery.models import Category


class AlbumTests(TestCase):

    def setUp(self) -> None:
        today = datetime.date.today()
        self.album = Album.objects.create(dirpath='foo', date=today)
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg')
        self.category = Category.objects.create(name="categorie")

        self.album.save()
        self.album.categories.add(self.category)

        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')

    def test_category(self):
        self.assertEqual(self.album.categories.all().count(), 1)

    def test_photo_urls(self):
        get_url = self.photo.get_signed_url()
        print(get_url)


