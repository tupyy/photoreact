import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.photo import Photo
from tests.base_testcase import BaseTestCase


class AlbumPermissionAPITest(BaseTestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='allowed_users')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')
        self.superman = User.objects.create_user('superman', 'batman@gallery', 'word')
        self.superman.groups.add(self.group)

        today = datetime.date.today()
        self.album = Album.objects.create(date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail_file')

        self.album.save()
        assign_perm('add_photos', self.batman, self.album)
        assign_perm('change_album', self.batman, self.album)
        assign_perm('add_photos', self.other, self.album)
        assign_perm('change_album', self.other, self.album)

        assign_perm('add_photos', self.group, self.album)
        assign_perm('change_album', self.group, self.album)

    def test_get_permission(self):
        """
        Description: Get permission for album id
        API:/permission/album/{id}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.get('/api/permission/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data[0]), 3)
        self.assertEqual(len(response.data[1]), 1)

    def test_get_permission_fail(self):
        """
        Description:  Get permission for a missing album
        API: /permission/album/{id}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 404
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.get('/api/permission/album/{}/'.format(self.album.id + 1))
        self.assertEqual(response.status_code, 404)

    def test_get_permission_fail2(self):
        """
        Description: Try to get permission by another user than the owner
        API: /permission/album/{}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username='other', password='word')
        client = self.get_client()
        response = client.get('/api/permission/album/{}/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_add_permission(self):
        """
        Description: Add permission
        API: /permission/album/{id}/
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.post('/api/permission/album/{}/'.format(self.album.id),
                               data=[
                                   {
                                       "user_id": self.batman.id,
                                       "permissions": ("delete_album",)
                                   },
                                   {
                                       "group_id": self.group.id,
                                       "permissions": ("delete_album",)
                                   }
                               ],
                               format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_permission(self):
        """
        Description: Delete permission
        API: /permission/album/{id}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.delete('/api/permission/album/{}/'.format(self.album.id),
                               data=[
                                   {
                                       "user_id": self.batman.id,
                                       "permissions": ("add_photos",)
                                   },
                                   {
                                       "group_id": self.group.id,
                                       "permissions": ("add_photos",)
                                   }
                               ],
                               format="json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.batman.has_perm("add_photos", self.album))
        self.assertTrue(self.batman.has_perm("change_album", self.album))

        # check permission for superman which is in group
        self.assertFalse(self.superman.has_perm("add_photos", self.album))
        self.assertTrue(self.superman.has_perm("change_album", self.album))

        # check permission for superman which is in group
        self.assertTrue(self.user.has_perm("add_photos", self.album))
        self.assertTrue(self.user.has_perm("change_album", self.album))

    def test_delete_permission2(self):
        """
        Description: Delete permission by another user than owner
        API: /permission/album/{id}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.delete('/api/permission/album/{}/'.format(self.album.id),
                               data=[
                                   {
                                       "user_id": self.user.id,
                                       "permissions": ("add_photos",)
                                   },
                                   {
                                       "group_id": self.group.id,
                                       "permissions": ("add_photos",)
                                   }
                               ],
                               format="json")
        self.assertEqual(response.status_code, 200)

        # check permission for superman which is in group
        self.assertFalse(self.superman.has_perm("add_photos", self.album))
        self.assertTrue(self.superman.has_perm("change_album", self.album))

        self.assertTrue(self.user.has_perm("add_photos", self.album))
        self.assertTrue(self.user.has_perm("change_album", self.album))
