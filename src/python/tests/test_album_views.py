import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from gallery.models import Album, Photo, AlbumAccessPolicy
from gallery.models import Category


class AlbumViewTests(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.date.today()
        self.album = Album.objects.create(dirpath='foo', date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg')
        self.category = Category.objects.create(name="categorie")

        self.album.save()
        self.album.categories.add(self.category)

    def test_get_album(self):
        client = APIClient()
        client.login(username='user', password='pass')
        request = client.get(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['id'], self.album.id)

    def test_get_album2(self):
        """ test the other user. no album found 404"""
        client = APIClient()
        client.login(username='other', password='word')
        request = client.get(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(request.status_code, 404)

    def test_get_albums3(self):
        """ get album by user which is allowed to view the album """
        policy = AlbumAccessPolicy.objects.create(album=self.album, public=False)
        policy.users.add(self.batman)

        client = APIClient()
        client.login(username='batman', password='word')
        request = client.get(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['id'], self.album.id)

    def test_list_albums(self):
        """ test get all albums by owner"""
        self.album2 = Album.objects.create(dirpath='bar', date=datetime.date.today(), owner=self.user, name='bar')
        client = APIClient()
        client.login(username='user', password='pass')
        request = client.get(reverse('album-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums2(self):
        """ test get all albums by batman"""
        album2 = Album.objects.create(dirpath='bar', date=datetime.date.today(), owner=self.user, name='bar')
        album2.save()
        policy1 = AlbumAccessPolicy.objects.create(album=self.album, public=False)
        policy1.users.add(self.batman)
        policy2 = AlbumAccessPolicy.objects.create(album=album2, public=False)
        policy2.users.add(self.batman)

        client = APIClient()
        client.login(username='batman', password='word')
        request = client.get(reverse('album-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums_404(self):
        """ test get all albums by other"""
        client = APIClient()
        client.login(username='other', password='word')
        request = client.get(reverse('album-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 0)
