import datetime

from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from guardian.shortcuts import assign_perm

from gallery.models.album import Album
from gallery.models.photo import Photo
from tests.base_testcase import BaseTestCase


class AlbumViewTests(BaseTestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.date.today()
        self.album = Album.objects.create(date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail_file')

        self.album.save()

    def test_get_album(self):
        """
        Description: Get album
        API: /api/album/{id}/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code:200
        Expected values:
        """
        assign_perm('view_album', self.user, self.album)
        self.login(username="user", password="pass")
        client = self.get_client()

        request = client.get(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['id'], self.album.id)

    def test_get_album2(self):
        """
        Description: Get album without permission
        API: /api/album/{id}
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username="other", password="word")
        client = self.get_client()
        request = client.get(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(request.status_code, 403)

    def test_list_albums(self):
        """
        Description: Get albums
        API: /api/albums/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 albums
        """
        assign_perm('view_album', self.user, self.album)

        album2 = Album.objects.create(date=datetime.date.today(), owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        self.login(username="user", password="pass")
        client = self.get_client()
        request = client.get(reverse('albums-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data['albums']), 2)

    def test_list_albums4(self):
        """
        Description: get albums with period filter
        API: albums?album_from=album_from_date&album_to=album_to_date
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1
        """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        self.login(username="user", password="pass")
        client = self.get_client()

        url = "{}?{}&{}".format(reverse('albums-list'),
                                "album_from=" + datetime.date.today().strftime("%Y-%m-%d"),
                                "album_to=" + datetime.date.today().strftime("%Y-%m-%d"))

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data.get('size'), 1)

    def test_album_list_limit(self):
        """
        Description: Test limit the queryset
        API: albums/?limit=1
        Method: GET
        Date: 25/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1
        """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        self.login(username="user", password="pass")
        client = self.get_client()
        url = "{}?{}".format(reverse('albums-list'),
                             "limit=1")

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data.get('size'), 1)

    def test_list_albums5(self):
        """
        Description: Get albums filtered by period
                      The request is made by a user different than owner which have "view_album" permissions
        API: /api/albums?album_from=album_from_date&album_to=album_to_date
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 album
        """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        self.login(username="user", password="pass")
        client = self.get_client()

        album_to_date = datetime.date.today() + datetime.timedelta(days=30)
        url = "{}?{}&{}".format(reverse('albums-list'),
                                "album_from=" + datetime.date.today().strftime("%Y-%m-%d"),
                                "album_to=" + album_to_date.strftime("%Y-%m-%d"))

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_list_albums_order_1(self):
        """
        Description: Test ordering by date
        API: /api/albums?ordering=name
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 album bar album is the first
        """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        self.login(username="user", password="pass")
        client = self.get_client()

        url = "{}?{}".format(reverse('albums-list'),
                             "ordering=name")

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['size'], 2)
        self.assertEqual(request.data['albums'][0]['id'], album2.id)

    def test_list_albums_order_2(self):
        """
        Description: Test ordering by date
        API: /api/albums?ordering=-date
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 album bar album is the first
        """
        assign_perm('view_album', self.user, self.album)

        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(date=album_date, owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        album2.save()
        self.login(username="user", password="pass")
        client = self.get_client()

        url = "{}?{}".format(reverse('albums-list'),
                             "ordering=name")

        request = client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['size'], 2)
        self.assertEqual(request.data['albums'][0]['id'], album2.id)

    def test_list_albums_404(self):
        """
        Description: Get albums by user with no view permission
        API: /api/albums/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 0 albums
        """
        self.login(username="other", password="word")
        client = self.get_client()
        request = client.get(reverse('albums-list'))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data.get('size'), 0)

    def test_list_albums_by_user(self):
        """
        Description: Get albums owned by user_id
        API: albums/user/{user_id}
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1
        """
        assign_perm('view_album', self.batman, self.album)
        self.login(username="batman", password="word")
        client = self.get_client()
        request = client.get(reverse('albums-get_by_user', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data.get('size'), 1)

    def test_list_albums_by_user2(self):
        """
        Description: Get albums by user with no view permission
        API: test API albums/user/{user_id}
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 0
        """
        self.login(username="batman", password="word")
        client = self.get_client()
        request = client.get(reverse('albums-get_by_user', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data.get('size'), 0)

    def test_list_albums_by_user3(self):
        """
        Description: Getting my own albums
        API: albums/user/{user_id}
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 0
        """
        self.login(username="user", password="pass")
        client = self.get_client()
        request = client.get(reverse('albums-get_by_user', args=(self.user.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data.get('size'), 1)

    def test_create_album(self):
        """
        Description: Create album
        API: /api/album/
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login(username="user", password="pass")
        client = self.get_client()

        content_type = ContentType.objects.get_for_model(Album)
        permission = Permission.objects.get(
            codename='add_album',
            content_type=content_type,
        )

        self.user.user_permissions.add(permission)
        data = dict()
        data['name'] = 'foo'
        data['date'] = datetime.date.today()
        data['description'] = "description"
        response = client.post(reverse('album-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        album = Album.objects.get(pk=response.data['id'])
        self.assertTrue(self.user.has_perm('add_permissions', album))

    def test_create_album_fail(self):
        """
        Description: Test create album when user has no permissions
        API: /api/album/
        Method:POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username="user", password="pass")
        client = self.get_client()
        data = dict()
        data['name'] = 'foo'
        data['date'] = datetime.date.today()
        response = client.post(reverse('album-list'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_album(self):
        """
        Description: Update album
        API: /api/albums/{id}
        Method: PUT
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        assign_perm('change_album', self.user, self.album)

        self.login(username="user", password="pass")
        client = self.get_client()
        data = dict()
        data['name'] = 'bar'
        data['date'] = datetime.date.today()
        response = client.patch(reverse('album-detail', args=[self.album.id]), data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_album(self):
        """
        Description: Delete album
        API: /api/album/{id}/
        Method: PUT
        Date: 19/08/2019
        User: cosmin
        Expected return code: 204 NO CONTENT
        Expected values:
        """
        assign_perm('delete_album', self.user, self.album)

        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.delete(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Album.objects.all()), 0)
        self.assertEqual(len(Photo.objects.all()), 0)

    def test_delete_album2(self):
        """
        Description: Delete album but no delete permission
        API: /api/album/{id}
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        self.login(username="batman", password="word")
        client = self.get_client()
        response = client.delete(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(response.status_code, 403)

    def test_post_albums(self):
        """
        Description: Get albums by id list
        API: /albums/
        Method: POST
        Date: 09/09/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1 album
        """
        assign_perm('view_album', self.user, self.album)

        album2 = Album.objects.create(date=datetime.date.today(), owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.post(reverse('albums-list'),
                               data={'ids': [1]},
                               format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('albums')), 1)

    def test_post_albums2(self):
        """
        Description: Get albums by id list
        API: /albums/
        Method: POST
        Date: 09/09/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 album
        """
        assign_perm('view_album', self.user, self.album)

        album2 = Album.objects.create(date=datetime.date.today(), owner=self.user, name='bar')
        assign_perm('view_album', self.user, album2)

        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.post(reverse('albums-list'),
                               data={'ids': [1, 2]},
                               format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('albums')), 2)

    def test_post_albums3(self):
        """
        Description: Get albums by id list. Request 2 albums but for the second the user has no view permission
        API: /albums/
        Method: POST
        Date: 09/09/2019
        User: cosmin
        Expected return code: 200
        Expected values: 1 album
        """
        assign_perm('view_album', self.user, self.album)

        album2 = Album.objects.create(date=datetime.date.today(), owner=self.batman, name='bar')
        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.post(reverse('albums-list'),
                               data={'ids': [1, 2]},
                               format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('albums')), 1)

    def test_post_albums4(self):
        """
        Description: Get albums by id list. Request with invalid data
        API: /albums/
        Method: POST
        Date: 09/09/2019
        User: cosmin
        Expected return code: 400
        Expected values:
        """
        assign_perm('view_album', self.user, self.album)

        album2 = Album.objects.create(date=datetime.date.today(), owner=self.user, name='bar')
        self.login(username="user", password="pass")
        client = self.get_client()
        response = client.post(reverse('albums-list'),
                               data={'ids': ["blaba"]},
                               format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_album_favorite(self):
        """
        Description: Get album. the album si favorite
        API: /api/album/{id}/
        Method: GET
        Date: 09/09/2019
        User: cosmin
        Expected return code:200
        Expected values:
        """
        from social.models import FavoriteAlbum

        assign_perm('view_album', self.user, self.album)
        favorite = FavoriteAlbum(user=self.user,
                                 album=self.album)
        favorite.save()
        self.login(username="user", password="pass")
        client = self.get_client()

        request = client.get(reverse('album-detail', args=[self.album.id]))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['id'], self.album.id)
        self.assertTrue(request.data.get('favorite'))
