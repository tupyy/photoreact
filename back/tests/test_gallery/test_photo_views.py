import datetime

from django.contrib.auth.models import Group, User
from guardian.shortcuts import assign_perm

from gallery.models.album import Album
from gallery.models.photo import Photo
from tests.base_testcase import BaseTestCase


class PhotoViewAPITest(BaseTestCase):

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
        """
        Description: Get photos of album id
        API: /photo/album/{id}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2
        """
        self.login(username="batman", password="word")
        client = self.get_client()
        response = client.get('/photos/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_photos2(self):
        """
        Description: Get photo of album. Superman has the right to view only one photo
                     through group "group"
        API: /photo/album/{id}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1
        """
        self.login(username="superman", password="word")
        client = self.get_client()
        response = client.get('/photos/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_photos_fail(self):
        """
        Description: Trying to get photo without view permission
        API: /photo/album/{id}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username="other", password="word")
        client = self.get_client()
        response = client.get('/photos/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_sign_photo(self):
        """
        Description: Test photo signing
        API: /photo/sign/album/{}/
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.post('/photo/sign/album/{}/'.format(self.album.id),
                               data={'filename': 'bar.jpg'},
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_sign_photo_admin(self):
        """
        Description: Test sign photo by a superuser
        API: /photo/sign/album/{}/
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        _ = User.objects.create_superuser('admin', 'user@gallery', 'pass')
        self.login(username="admin", password="pass")
        client = self.get_client()
        response = client.post('/photo/sign/album/{}/'.format(self.album.id),
                               data={'filename': 'bar.jpg'},
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_sign_photo_fail(self):
        """
        Description: Try to sign a photo for an album for which the current user has no "add_photos" permission
        API: /photo/sign/album/{}
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username="batman", password="word")
        client = self.get_client()
        response = client.post('/photo/sign/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_add_photo(self):
        """
        Description: Test add photo api
        API: /photo/album/{}/
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.post('/photo/album/{}/'.format(self.album.id),
                               data={'filename': 'bar.jpg',
                                     'thumbnail': 'test.jpg'},
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_photo(self):
        """
        Description: Delete photo
        API:/photo/{id}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 204
        Expected values:
        """
        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.delete('/photo/{}/'.format(self.photo.id))
        self.assertEqual(response.status_code, 204)

    def test_delete_photo_no_permission(self):
        """
        Description: Delete photo but no "delete_photo" permission
        API: /photo/{id}
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username="other", password="word")
        client = self.get_client()
        response = client.delete('/photo/{}/'.format(self.photo.id))
        self.assertEqual(response.status_code, 403)

    def test_delete_photo_assign_permission(self):
        """
        Description: Delete photo but assign permission
        API: /photo/{id}
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 204
        Expected values:
        """
        assign_perm('delete_photos', self.batman, self.album)
        self.login(username="batman", password="word")
        client = self.get_client()
        response = client.delete('/photo/{}/'.format(self.photo.id))
        self.assertEqual(response.status_code, 204)
