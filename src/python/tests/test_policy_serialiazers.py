import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase

from gallery.models import Album, Photo, AlbumAccessPolicy
from gallery.models import Category
from gallery.serializers.policy_serializers import AlbumAccessPolicySerializer


class PolicySerializersTests(TestCase):

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

    def test_access_policy(self):
        """ get album by user which is allowed to view the album """
        policy = AlbumAccessPolicy.objects.create(album=self.album, public=False)
        policy.users.add(self.batman)

        serializer = AlbumAccessPolicySerializer(policy)
        self.assertEqual(serializer.data['album_id'], self.album.id)
        self.assertEqual(serializer.data['users'][0]['id'], self.batman.id)