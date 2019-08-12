import datetime

from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.photo import Photo


class AlbumViewTests(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.date.today()
        self.album = Album.objects.create(folder_path='foo', date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail_file')

        self.album.save()

    def test_get_album(self):
        assign_perm('view_album', self.user, self.album)
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
        self.assertEqual(request.status_code, 403)

    def test_list_albums(self):
        """ test get all albums by owner"""
        assign_perm('view_album', self.user, self.album)

        album2 = Album.objects.create(folder_path='bar', date=datetime.date.today(), owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        client = APIClient()
        client.login(username='user', password='pass')
        request = client.get(reverse('albums-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums6(self):
        album2 = Album.objects.create(folder_path='bar', date=datetime.date.today(), owner=self.user, name='bar')

        client = APIClient()
        client.login(username='user', password='pass')
        request = client.get(reverse('albums-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums4(self):
        """ filter by period """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(folder_path='bar', date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        url = "{}?{}&{}".format(reverse('albums-list'),
                                "start=" + datetime.date.today().strftime("%d-%m-%Y"),
                                "end=" + datetime.date.today().strftime("%d-%m-%Y"))

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_list_albums5(self):
        """ filter by period """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(folder_path='bar', date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        client = APIClient()
        client.login(username='user', password='pass')

        end_date = datetime.date.today() + datetime.timedelta(days=30)
        url = "{}?{}&{}".format(reverse('albums-list'),
                                "start=" + datetime.date.today().strftime("%d-%m-%Y"),
                                "end=" + end_date.strftime("%d-%m-%Y"))

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums_404(self):
        """ test get all albums by other"""
        client = APIClient()
        client.login(username='other', password='word')
        request = client.get(reverse('albums-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 0)

    def test_list_albums_by_user(self):
        """ test API albums/user/{user_id}"""
        assign_perm('view_album', self.batman, self.album)
        client = APIClient()
        client.login(username='batman', password='word')
        request = client.get(reverse('albums-get_by_user', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_list_albums_by_user2(self):
        """ test API albums/user/{user_id}
            Log as batman with no with permission.
            Should get 200 but 0 albums
        """
        client = APIClient()
        client.login(username='batman', password='word')
        request = client.get(reverse('albums-get_by_user', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 0)

    def test_list_albums_by_user3(self):
        """ test API albums/user/{user_id}
            Log as user.
            Should get 200 but 1 albums ( I'm getting my own albums)
        """
        client = APIClient()
        client.login(username='user', password='pass')
        request = client.get(reverse('albums-get_by_user', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)

    def test_create_album(self):
        client = APIClient()
        client.login(username='user', password='pass')

        content_type = ContentType.objects.get_for_model(Album)
        permission = Permission.objects.get(
            codename='add_album',
            content_type=content_type,
        )

        self.user.user_permissions.add(permission)
        data = dict()
        data['name'] = 'foo'
        data['folder_path'] = 'folder_path'
        data['date'] = datetime.date.today()
        response = client.post(reverse('album-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        album = Album.objects.get(pk=response.data['id'])
        self.assertTrue(self.user.has_perm('add_permissions', album))

    def test_create_album_fail(self):
        """ Test create album when user has no permissions"""
        client = APIClient()
        client.login(username='user', password='pass')
        data = dict()
        data['name'] = 'foo'
        data['folder_path'] = 'folder_path'
        data['date'] = datetime.date.today()
        response = client.post(reverse('album-list'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_album(self):
        assign_perm('change_album', self.user, self.album)

        client = APIClient()
        client.login(username='user', password='pass')
        data = dict()
        data['name'] = 'bar'
        data['tags'] = ({'name': 'foo'},)
        data['date'] = datetime.date.today()
        response = client.patch(reverse('album-detail', args=[self.album.id]), data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_album(self):
        assign_perm('delete_album', self.user, self.album)

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
        self.assertEqual(response.status_code, 403)
