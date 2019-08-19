from datetime import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase

from gallery.models.album import ActivityLog
from gallery.models.album import Album
from gallery.models.photo import Photo
from gallery.serializers.log_serializer import ActivityLogSerializer


class TestAlbumSerializer(TestCase):

    def setUp(self) -> None:
        self.group = Group.objects.create(name='group')
        self.user = User.objects.create_user('user', 'user@gallery', 'pass')
        self.user.groups.add(self.group)
        self.other = User.objects.create_user('other', 'other@gallery', 'word')
        self.batman = User.objects.create_user('batman', 'batman@gallery', 'word')

        today = datetime.today()
        self.album = Album.objects.create(folder_path='foo', date=today.date(), owner=self.user, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail')

        self.album.save()

    def test_serializer_fields(self):
        """
        Description: test some of the serializer fields
        Date: 19/08/2019
        User: cosmin
        Expect:
        """
        activity_log = ActivityLog(content_object=self.album, activity='C', user=self.user)
        activity_log.save()

        activity_serializer = ActivityLogSerializer(activity_log)
        self.assertTrue(activity_serializer.data is not None)
        self.assertEqual(activity_serializer.data['activity'], 'C')

    def test_serializer_fields_2(self):
        activity_log = ActivityLog(content_object=self.photo, activity='C', user=self.user)
        activity_serializer = ActivityLogSerializer(activity_log)
        self.assertTrue(activity_serializer.data is not None)
        self.assertEqual(activity_serializer.data['activity'], 'C')
