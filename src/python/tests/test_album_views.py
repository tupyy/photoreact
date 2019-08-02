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
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail='thumbnail')
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

    def test_list_albums3(self):
        """ test get all albums owned by other and can be accessed by batman"""
        album2 = Album.objects.create(dirpath='bar', date=datetime.date.today(), owner=self.other, name='bar')
        album2.save()
        policy1 = AlbumAccessPolicy.objects.create(album=self.album, public=False)
        policy1.users.add(self.batman)
        policy2 = AlbumAccessPolicy.objects.create(album=album2, public=False)
        policy2.users.add(self.batman)

        client = APIClient()
        client.login(username='batman', password='word')

        url = "{}?{}".format(reverse('album-list'), "owner=" + str(self.user.id))
        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_list_albums4(self):
        """ filter by period """
        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(dirpath='bar', date=album_date, owner=self.user, name='bar')
        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        url = "{}?{}&{}".format(reverse('album-list'),
                                "start_date=" + datetime.date.today().strftime("%d-%m-%Y"),
                                "end_date=" + datetime.date.today().strftime("%d-%m-%Y"))

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_list_albums5(self):
        """ filter by period """
        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(dirpath='bar', date=album_date, owner=self.user, name='bar')
        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        end_date = datetime.date.today() + datetime.timedelta(days=30)
        url = "{}?{}&{}".format(reverse('album-list'),
                                "start_date=" + datetime.date.today().strftime("%d-%m-%Y"),
                                "end_date=" + end_date.strftime("%d-%m-%Y"))

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums6(self):
        """ filter by category single query parameter """
        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(dirpath='bar', date=album_date, owner=self.user, name='bar')
        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        url = "{}?{}".format(reverse('album-list'),
                             "category=categorie")
        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_list_albums7(self):
        """ filter by category single query parameter """
        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(dirpath='bar', date=album_date, owner=self.user, name='bar')
        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        url = "{}?{}".format(reverse('album-list'),
                             "category=bar")
        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 0)

    def test_list_albums8(self):
        """ filter by category multiple query parameter """
        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(dirpath='bar', date=album_date, owner=self.user, name='bar')
        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        url = "{}?{}&{}".format(reverse('album-list'),
                                "category=bar",
                                "category=categorie")
        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_list_albums_404(self):
        """ test get all albums by other"""
        client = APIClient()
        client.login(username='other', password='word')
        request = client.get(reverse('album-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 0)

    def test_create_album(self):
        client = APIClient()
        client.login(username='user', password='pass')
        data = dict()
        data['name'] = 'foo'
        data['dirpath'] = 'dirpath'
        data['categories'] = list()
        data['tags'] = list()
        data['date'] = datetime.date.today()
        response = client.post(reverse('album-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_album(self):
        client = APIClient()
        client.login(username='user', password='pass')
        data = dict()
        data['name'] = 'bar'
        data['tags'] = ({'name': 'foo'},)
        data['date'] = datetime.date.today()
        data['categories'] = ({'name': 'foo'},)
        response = client.patch(reverse('album-detail', args=[self.album.id]), data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_create_album2(self):
        client = APIClient()
        client.login(username='user', password='pass')
        data = dict()
        data['name'] = 'foo'
        data['dirpath'] = 'dirpath'
        data['tags'] = ({'name': 'foo'},)
        data['date'] = datetime.date.today()
        data['categories'] = ({'name': 'foo'},)
        response = client.post(reverse('album-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_album2(self):
        category = Category.objects.create(name='bar')
        self.album.categories.add(category)
        self.album.save()

        client = APIClient()
        client.login(username='user', password='pass')
        data = dict()
        data['name'] = 'bar'
        data['tags'] = ({'name': 'foo'},)
        data['date'] = datetime.date.today()
        data['categories'] = ({'name': 'foo'},)
        response = client.patch(reverse('album-detail', args=[self.album.id]), data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_album3(self):
        """ only the owner can update its album """
        category = Category.objects.create(name='bar')
        self.album.categories.add(category)
        self.album.save()

        client = APIClient()
        client.login(username='batman', password='word')
        data = dict()
        data['name'] = 'bar'
        data['tags'] = ({'name': 'foo'},)
        data['date'] = datetime.date.today()
        data['categories'] = ({'name': 'foo'},)
        response = client.patch(reverse('album-detail', args=[self.album.id]), data=data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_update_album4(self):
        """
            only the owner can update its album
            Test the access policy
        """
        policy = AlbumAccessPolicy.objects.create(album=self.album, public=False)
        policy.users.add(self.batman)

        client = APIClient()
        client.login(username='batman', password='word')
        data = dict()
        data['name'] = 'bar'
        data['tags'] = ({'name': 'foo'},)
        data['date'] = datetime.date.today()
        data['categories'] = ({'name': 'foo'},)
        response = client.patch(reverse('album-detail', args=[self.album.id]), data=data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_delete_album(self):
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.delete(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Album.objects.all()), 0)
        self.assertEqual(len(Photo.objects.all()), 0)

    def test_delete_album2(self):
        """ Only owner has the right to delete the album """
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.delete(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(response.status_code, 404)
