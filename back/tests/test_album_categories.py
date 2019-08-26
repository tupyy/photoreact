import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models.category import Category
from gallery.models.photo import Photo


class AlbumCategoryAPITest(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.date.today()
        self.album = Album.objects.create(folder_path='foo', date=today, owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail_file')

        self.category_foo = Category.objects.create(name="foo")
        self.category_bar = Category.objects.create(name="bar")

        self.album.save()
        self.album.categories.add(self.category_bar, self.category_foo)

    def test_get_categories(self):
        """
        Description: Get basic categories
        API: /album/{]/categories/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 categories
        """
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.get('/album/{}/categories/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_categories_fail(self):
        """
        Description: Test get categories when user has no view permission on the album
        API: /album/{}/categories/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.get('/album/{}/categories/'.format(self.album.id))
        self.assertEqual(response.status_code, 403)

    def test_get_categories_404(self):
        """
        Description: Test get categories when album do not exists
        API: /album/{}/categories/
        Method: GET
        Date: 19/08/2019
        User: cosmin
        Expected return code: 404
        Expected values:
        """
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.get('/album/{}/categories/'.format(100))
        self.assertEqual(response.status_code, 404)

    def test_add_categories(self):
        """
        Description: Add new category to album
        API: /album/{}/category
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        client = APIClient()
        client.login(username='user', password='pass')
        data = list()
        cat1 = Category.objects.create(name="hey")
        data.append(cat1.name)
        response = client.post('/album/{}/category/'.format(self.album.id),
                               data=data,
                               format='json')
        self.assertEqual(response.status_code, 200)

    def test_add_categories2(self):
        """
        Description: Test add new categories without permission
        API: /album/{}/category
        Method: POST
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        assign_perm('view_album', self.batman, self.album)
        client = APIClient()
        client.login(username='batman', password='word')
        data = list()
        data.append("test")
        response = client.post('/album/{}/category/'.format(self.album.id),
                               data=data,
                               format='json')
        self.assertEqual(response.status_code, 403)

    def test_delete_category(self):
        """
        Description: Remove category from album
        API: /album/{id}/category/{name category}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200 OK
        Expected values: 1 category left
        """
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.delete('/album/{}/category/{}/'.format(self.album.id,
                                                                 self.category_foo.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.album.categories.count(), 1)

    def test_delete_category_fail(self):
        """
        Description: Test delete category with no permission
        API: /album/{id}/category/{name category}/
        Method: DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 403
        Expected values:
        """
        assign_perm('view_album', self.batman, self.album)
        client = APIClient()
        client.login(username='batman', password='word')
        response = client.delete('/album/{}/category/{}/'.format(self.album.id,
                                                                 self.category_foo.id))
        self.assertEqual(response.status_code, 403)

    def test_put_category(self):
        """
        Description: Change category
        API: /album/{id}/category/{name category}/
        Method: PUT
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 2 categories. the last one is replaced by the new one
        """
        new_cat = Category.objects.create(name="hey")
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.put('/album/{}/category/{}/'.format(self.album.id,
                                                              self.category_foo.id),
                              data={'category_id': new_cat.id},
                              format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.album.categories.count(), 2)
        self.assertEqual(self.album.categories.last().name, 'hey')

    def test_favorites_post(self):
        """
        Description: Test both POST and DELETE favorite API
        API: /album/{}/favorites
        Method: POST / DELETE
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        client = APIClient()
        client.login(username='user', password='pass')
        response = client.post('/album/{}/favorites/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user in self.album.favorites.all())

        # test delete favorites
        response = client.delete('/album/{}/favorites/'.format(self.album.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user in self.album.favorites.all())