import random
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from gallery.models.album import Album
from gallery.models import ActivityLog
from gallery.models.photo import Photo


class TestAlbumSerializer(TestCase):

    def setUp(self) -> None:
        self.batman = User.objects.create_superuser('batman', 'batman@gothamcity.org', 'pass')
        self.superman = User.objects.create_user('superman', 'superman@kryption.org', 'pass')

        today = datetime.today()
        self.album = Album.objects.create(folder_path='foo', date=today.date(), owner=self.batman, name='foo')
        self.photo = Photo.objects.create(album=self.album, filename='bar.jpg', thumbnail_file='thumbnail')

        self.album.save()
        activity_types = ['C', 'D', 'V', 'U']
        models = [self.album, self.photo]

        for user in [self.batman, self.superman]:
            for i in range(100):
                model = models[random.randint(0, 1)]
                activity_type = activity_types[random.randint(0, 3)]
                activity_log = ActivityLog(content_object=model,
                                           user=user,
                                           activity=activity_type,
                                           date=self.random_date(datetime.today() - timedelta(days=60), datetime.today())
                                           )
                activity_log.save()

    def test_get_activities(self):
        """
        Description: Test basic GET API
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200 OK
        Expected values: 200 activities logs on 2 pages
        """
        client = APIClient()
        client.login(username='batman', password='pass')
        response = client.get('/activities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 200)
        self.assertTrue(response.data.get('total_pages') is not None)
        self.assertEqual(response.data.get('total_pages'), 2)
        self.assertTrue(response.data.get('current_page') is not None)
        self.assertEqual(response.data.get('current_page'), 1)

    def test_get_activities_2(self):
        """
        Description: Test GET API with end date before the first date of the queryset
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: 0 activity log entries
        """
        client = APIClient()
        client.login(username='batman', password='pass')
        response = client.get('/activities/?end=01/01/2019')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_get_activities_3(self):
        """
        Description: Test GET API. The logged user is not superuser so we expect the queryset to be filtered
        Date: 19/08/2019
        User: cosmin
        Expected return code: 200 OK
        Expected values: 100 entries. Only the superman entries
        """
        client = APIClient()
        client.login(username='superman', password='pass')
        response = client.get('/activities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 100)

    def test_get_activityes_filter(self):
        """
        Description: Test activity type filter
        API: /activities/?activity_type=C
        Method: GET
        Date: 25/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        client = APIClient()
        client.login(username='superman', password='pass')
        response = client.get('/activities/?activity=C')
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        for result in results:
            self.assertEqual(result.get('activity'), 'C')

    def random_date(self, start_date, end_date):
        timestamp_start = start_date.timestamp()
        timestamp_end = end_date.timestamp()
        random_timestamp = timestamp_start + random.random() * (timestamp_end - timestamp_start)
        return datetime.utcfromtimestamp(random_timestamp)
