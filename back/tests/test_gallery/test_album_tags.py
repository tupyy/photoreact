import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.category import Tag
from gallery.models.photo import Photo
from tests.base_testcase import BaseTestCase


class AlbumTagAPITest(BaseTestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.date.today()
        self.album = Album.objects.create(folder_path='foo', date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail_file')

        self.tag_foo = Tag.objects.create(name="foo")
        self.tag_bar = Tag.objects.create(name="bar")

        self.album.save()
        self.album.tags.add(self.tag_bar, self.tag_foo)

    def test_get_tags(self):
        """
        Description: Get tag of album id
        API: /album/{id}/tags
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 tags
        """
        self.login(username='user', password='pass')
        client = self.get_client()

        response = client.get('/album/{}/tags/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_tags_fail(self):
        """
        Description: Get albums tags no view permission
        API: /album/{id}/tags
        Method:
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username='batman', password='word')
        client = self.get_client()
        response = client.get('/album/{}/tags/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_get_tags_404(self):
        """
        Description: Get a missing album
        API: /album/{id}/tags
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 404
        Expected values:
        """
        self.login(username='batman', password='word')
        client = self.get_client()
        response = client.get('/album/{}/tags/'.format(100))
        self.assertEqual(response.status_code, 404)

    def test_add_tags(self):
        """
        Description: Add tags
        API: /album/{id}/tags
        Method:POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        data = list()
        tag1 = Tag.objects.create(name="hey")
        data.append(tag1.name)
        response = client.post('/album/{}/tag/'.format(self.album.id),
                               data=data,
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_add_tags2(self):
        """
        Description: Add tag . Create tag because it doesn't exist
        API: /album/{id}/tags
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        data = list()
        data.append("hey")
        response = client.post('/album/{}/tag/'.format(self.album.id),
                               data=data,
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_add_tags3(self):
        """
        Description: Try to add tag when user hasn't "change" permission
        API: /album/{id}/tags
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        assign_perm('view_album', self.batman, self.album)
        self.login(username='batman', password='word')
        client = self.get_client()
        data = list()
        data.append("test")
        response = client.post('/album/{}/tag/'.format(self.album.id),
                               data=data,
                               format='json')
        self.assertEqual(response.status_code, 403)

    def test_delete_tag(self):
        """
        Description: Delete tag
        API: /album/{id}/tag/{id tag}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1 tag left
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.delete('/album/{}/tag/{}/'.format(self.album.id,
                                                                 self.tag_foo.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.album.tags.count(), 1)

    def test_delete_tag_fail(self):
        """
        Description: Delete tag when user hasn't no permission
        API: /album/{id}/tag/{id tag}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        assign_perm('view_album', self.batman, self.album)
        self.login(username='batman', password='word')
        client = self.get_client()
        response = client.delete('/album/{}/tag/{}/'.format(self.album.id,
                                                                 self.tag_foo.id))
        self.assertEqual(response.status_code, 403)

    def test_put_tag(self):
        """
        Description: Change tag
        API: /album/{id}/tag/{id tag}/
        Method: PUT
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        new_tag = Tag.objects.create(name="hey")
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.put('/album/{}/tag/{}/'.format(self.album.id,
                                                              self.tag_foo.id),
                              data={'tag_name': new_tag.name},
                              format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.album.tags.count(), 2)
        self.assertEqual(self.album.tags.last().name, 'hey')

    def test_put_tag2(self):
        """
        Description: Change tag
        API: /album/{id}/tag/{id tag}/
        Method: PUT
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 tags
        """
        self.login(username='user', password='pass')
        client = self.get_client()
        response = client.put('/album/{}/tag/{}/'.format(self.album.id,
                                                              self.tag_foo.id),
                              data={'tag_name': "hey"},
                              format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.album.tags.count(), 2)
        self.assertEqual(self.album.tags.last().name, 'hey')

