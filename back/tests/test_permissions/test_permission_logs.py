import random
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User, Permission

from accounts.models import UserProfile
from activity_log.models import ActivityLog
from gallery.models.album import Album
from permissions.models import PermissionLog
from tests.base_testcase import BaseTestCase


class TestAlbumSerializer(BaseTestCase):

    def setUp(self) -> None:
        self.batman = User.objects.create_superuser('batman', 'batman@gothamcity.org', 'pass')
        self.superman = User.objects.create_user('superman', 'superman@kryption.org', 'pass')

        today = datetime.today()
        self.album = Album.objects.create(date=today.date(), owner=self.batman, name='foo')
        self.album.save()

        permission_log1 = PermissionLog(content_object=self.batman,
                                        user_from=self.superman,
                                        album=self.album,
                                        permission=Permission.objects.first(),
                                        operation=PermissionLog.ADD)

        user_profile = UserProfile.objects.create(user=self.batman,
                                                  photo_filename="foo.jpg")
        user_profile.save()
        permission_log1.save()

    def test_get_log1(self):
        """
        Description: test get list permission
        API: /permission/log/
        Method: GET
        Date: 18/09/2019
        User: cosmin
        Expected return code: 200
        Expected values: log for the current user only
        """
        self.login("superman", "pass")
        client = self.get_client()
        response = client.get("/api/permission/log/")
        self.assertEqual(response.status_code, 200)

        logs = response.data.get('logs')
        self.assertFalse(logs is None)
        self.assertEqual(logs[0].get('user_from'), 'superman')
        self.assertFalse(logs[0].get('content_object').get('profile') is None)
        self.assertEqual(logs[0].get('content_object').get('profile').get('username'), 'batman')
