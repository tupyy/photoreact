import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.photo import Photo


class PhotoViewAPITest(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='allowed_users')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')

        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        self.superman = User.objects.create_user('superman', 'batman@gallery', 'word')
        self.superman.groups.add(self.group)

        today = datetime.date.today()
        self.album = Album.objects.create(folder_path='foo', date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail_file')
        self.photo2 = Photo.objects.create(album=self.album, filename='foo.jpg', thumbnail_file='thumbnail_file')

        self.album2 = Album.objects.create(folder_path='bar', date=today, owner=self.user, name='bar')
        self.photo_album2 = Photo.objects.create(album=self.album2, filename='bar2.jpg',
                                                 thumbnail_file='thumbnail_file')
        self.photo2_album_2 = Photo.objects.create(album=self.album2, filename='foo2.jpg',
                                                   thumbnail_file='thumbnail_file')

        self.album.save()
        self.album2.save()

        assign_perm('view_album', self.batman, self.album)
        assign_perm('gallery.view_photo', self.batman, self.photo)
        assign_perm('gallery.view_photo', self.batman, self.photo2)

        assign_perm('view_album', self.batman, self.album2)
        assign_perm('gallery.view_photo', self.batman, self.photo_album2)
        assign_perm('gallery.view_photo', self.batman, self.photo2_album_2)

        assign_perm('view_album', self.group, self.album)
        assign_perm('gallery.view_photo', self.group, self.photo)

    def test_get_photos(self):
        """ GET /photo/album/{id}/ """
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.get('/photos/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_photos2(self):
        """ GET /photo/album/{id}/ """
        client = APIClient()
        client.login(username='superman', password='word')
        response = client.get('/photos/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_photos_fail(self):
        """ GET /photo/album/{id}/
            No view_album permission
        """
        client = APIClient()
        client.login(username='other', password='word')
        response = client.get('/photos/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_sign_photo(self):
        """
        test sign url for post method
        """
        client = APIClient()
        client.login(username="user", password="pass")
        response = client.post('/photo/sign/album/{}/'.format(self.album.id),
                               data={'filename': 'bar.jpg'},
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_sign_photo_admin(self):
        """
        test sign url for post method
        """
        admin = User.objects.create_superuser('admin', 'user@gallery', 'pass')
        client = APIClient()
        client.login(username="admin", password="pass")
        response = client.post('/photo/sign/album/{}/'.format(self.album.id),
                               data={'filename': 'bar.jpg'},
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_sign_photo_fail(self):
        """
        no permission => 403
        """
        client = APIClient()
        client.login(username="batman", password="word")
        response = client.post('/photo/sign/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_add_photo(self):
        """
        test add post method
        """
        client = APIClient()
        client.login(username="user", password="pass")
        response = client.post('/photo/album/{}/'.format(self.album.id),
                               data={'filename': 'bar.jpg',
                                     'thumbnail': 'test.jpg'},
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_photo(self):
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.delete('/photo/{}/'.format(self.photo.id))
        self.assertEqual(response.status_code, 204)

    def test_delete_photo_no_permission(self):
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.delete('/photo/{}/'.format(self.photo.id))
        self.assertEqual(response.status_code, 403)

    def test_delete_photo_assign_permission(self):
        assign_perm('delete_photos', self.batman, self.album)
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.delete('/photo/{}/'.format(self.photo.id))
        self.assertEqual(response.status_code, 204)
