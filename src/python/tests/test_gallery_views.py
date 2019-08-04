import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.photo import Photo
from gallery.models.category import Category


class GalleryTests(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')

        today = datetime.date.today()
        self.album = Album.objects.create(dirpath='foo', date=today, owner=self.user)
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail='thumbnail')
        self.category = Category.objects.create(name="categorie")

        self.album.save()
        self.album.categories.add(self.category)

    def test_get_album(self):
        client = APIClient()
        client.login(username='user', password='pass')
        request = client.get('/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_get_album2(self):
        """ Log the other user. should get empty response"""
        client = APIClient()
        client.login(username='other', password='word')
        request = client.get('/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 0)

