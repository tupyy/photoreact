from django.contrib.auth.models import User

from gallery.models.album import Album
from tests.base_testcase import BaseTestCase
import datetime


class AlbumViewTests(BaseTestCase):

    def test_album_folder_name(self):
        """
        Description: Test folder_path property
        API: N/A
        Method: N/A
        Date: 02/09/2019
        User: cosmin
        Expected return code: N/A
        Expected values: folder_path as year/month_date_name
        """
        user = User.objects.create(username="user",password="word")
        user.save()
        album_date = datetime.date.today() + datetime.timedelta(days=10)
        album2 = Album.objects.create(date=album_date, owner=user, name='bar')
        self.assertEqual(album2.folder_path, "{}/{}_{}_{}".format(str(album_date.year),
                                                                  str(album_date.month),
                                                                  str(album_date.day),
                                                                  "bar"))
