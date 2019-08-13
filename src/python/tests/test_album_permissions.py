import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.category import Tag
from gallery.models.photo import Photo


class AlbumPermissionAPITest(TestCase):

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

        self.album.save()
        assign_perm('add_photos', self.batman, self.album)
        assign_perm('change_album', self.batman, self.album)
        assign_perm('add_photos', self.other, self.album)
        assign_perm('change_album', self.other, self.album)

        assign_perm('add_photos', self.group, self.album)
        assign_perm('change_album', self.group, self.album)

    def test_get_permissions(self):
        """ GET /album/{id}/permissions """
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.get('/album/{}/permissions/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data[0]), 3)
        self.assertEqual(len(response.data[1]), 1)
        self.assertEqual(response.data[0][2]['username'], 'other')

    def test_get_permissions_fail(self):
        """ GET /album/{id}/permissions
            Album not found
        """
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.get('/album/{}/permissions/'.format(self.album.id + 1))
        self.assertEqual(response.status_code, 404)

    def test_get_permissions_fail2(self):
        """ GET /album/{id}/permissions
            Not owner
        """
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.get('/album/{}/permissions/'.format(self.album.id + 1))
        self.assertEqual(response.status_code, 403)

    def test_add_permissions(self):
        """ POST /album/{id}/permissions """
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.post('/album/{}/permissions/'.format(self.album.id),
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

    # def test_get_tags_fail(self):
    #     """
    #         GET /album/{id}/tags
    #         Expected: 403 no permissions
    #     """
    #     client = APIClient()
    #     client.login(username='batman', password='word')
    #     response = client.get('/album/{}/tags/'.format(self.album.id))
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_get_tags_404(self):
    #     """
    #         GET /album/{id}/tags
    #         Expected: 403 no permissions
    #     """
    #     client = APIClient()
    #     client.login(username='batman', password='word')
    #     response = client.get('/album/{}/tags/'.format(100))
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_add_tags(self):
    #     """ POST /album/{id}/tag """
    #     client = APIClient()
    #     client.login(username='user', password='pass')
    #     data = list()
    #     tag1 = Tag.objects.create(name="hey")
    #     data.append(tag1.name)
    #     response = client.post('/album/{}/tag/'.format(self.album.id),
    #                            data=data,
    #                            format='json')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_add_tags2(self):
    #     """ POST /album/{id}/tag
    #         Tag do not exits. create it..
    #     """
    #     client = APIClient()
    #     client.login(username='user', password='pass')
    #     data = list()
    #     data.append("hey")
    #     response = client.post('/album/{}/tag/'.format(self.album.id),
    #                            data=data,
    #                            format='json')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_add_tags3(self):
    #     """
    #         POST /album/{id}/tag
    #         Fail no permission
    #
    #      """
    #     assign_perm('view_album', self.batman, self.album)
    #     client = APIClient()
    #     client.login(username='batman', password='word')
    #     data = list()
    #     data.append("test")
    #     response = client.post('/album/{}/tag/'.format(self.album.id),
    #                            data=data,
    #                            format='json')
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_delete_tag(self):
    #     """ DELETE /album/{id}/tag/{id tag}/ """
    #     client = APIClient()
    #     client.login(username='user', password='pass')
    #     response = client.delete('/album/{}/tag/{}/'.format(self.album.id,
    #                                                              self.tag_foo.id))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(self.album.tags.count(), 1)
    #
    # def test_delete_tag_fail(self):
    #     """ DELETE /album/{id}/tag/{id tag}/
    #         Fail no permission
    #     """
    #     assign_perm('view_album', self.batman, self.album)
    #     client = APIClient()
    #     client.login(username='batman', password='word')
    #     response = client.delete('/album/{}/tag/{}/'.format(self.album.id,
    #                                                              self.tag_foo.id))
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_put_tag(self):
    #     """ PUT /album/{id}/tag/{id tag}/ """
    #     new_tag = Tag.objects.create(name="hey")
    #     client = APIClient()
    #     client.login(username='user', password='pass')
    #     response = client.put('/album/{}/tag/{}/'.format(self.album.id,
    #                                                           self.tag_foo.id),
    #                           data={'tag_name': new_tag.name},
    #                           format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(self.album.tags.count(), 2)
    #     self.assertEqual(self.album.tags.last().name, 'hey')
    #
    # def test_put_tag2(self):
    #     """ PUT /album/{id}/tag/{id tag}/ """
    #     client = APIClient()
    #     client.login(username='user', password='pass')
    #     response = client.put('/album/{}/tag/{}/'.format(self.album.id,
    #                                                           self.tag_foo.id),
    #                           data={'tag_name': "hey"},
    #                           format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(self.album.tags.count(), 2)
    #     self.assertEqual(self.album.tags.last().name, 'hey')
