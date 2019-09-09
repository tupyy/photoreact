import random
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from storages.backends.s3boto3 import S3Boto3Storage

from gallery.models.album import Album
from gallery.models.photo import Photo


class Command(BaseCommand):
    """
    Create albums based on the bucket content
    """

    def handle(self, *args, **options):
        photo_storage = S3Boto3Storage(location="photos")
        cache_storage = S3Boto3Storage(location="caches")

        photo_data = self.read_bucket_content(photo_storage, "", None)
        cache_data = self.read_bucket_content(cache_storage, "", None)

        user = User.objects.first()

        # for each key except year key we create an album
        albums = list()
        for k, v in photo_data.items():
            if self.is_year(k):
                albums = self.create_albums(user, k, v)

        for album in albums:
            photos_and_thumbnails = self.get_photos_and_thumbnail(album, photo_data, cache_data)
            for entry in photos_and_thumbnails:
                photo = Photo.objects.create(filename=entry[1],
                                             date=album.date,
                                             album=album,
                                             thumbnail_file=entry[2])
                photo.save()

    def read_bucket_content(self, storage, root_folder, data=None):
        if data is None:
            data = dict()

        folders, files = storage.listdir(root_folder)
        for file in files:
            if data.get('files') is None:
                data['files'] = list()
            data.get('files').append(file)

        for folder in folders:
            data[folder] = dict()
            new_folder = "{}/{}".format(root_folder, folder).lstrip('/')
            _ = self.read_bucket_content(storage, new_folder, data[folder])

        return data

    def random_date(self, start_date, end_date):
        timestamp_start = start_date.timestamp()
        timestamp_end = end_date.timestamp()
        random_timestamp = timestamp_start + random.random() * (timestamp_end - timestamp_start)
        return datetime.utcfromtimestamp(random_timestamp)

    def is_year(self, year_str):
        try:
            datetime.strptime(year_str, '%Y')
            return True
        except ValueError:
            return False

    def create_albums(self, owner, album_year, album_data):
        albums = list()
        for k, v in album_data.items():
            end_album_date_str = "{}/{}/{}".format(datetime.today().day,
                                                   datetime.today().month,
                                                   album_year if album_year else datetime.today().year)
            end_album_date = datetime.strptime(end_album_date_str, "%d/%m/%Y")
            start_album_date = datetime.strptime(
                "01/01/{}".format(album_year if album_year else datetime.today().year),
                "%d/%m/%Y")
            album_date = self.random_date(start_album_date, end_album_date)
            album, _ = Album.objects.get_or_create(name= k,
                                                    defaults={
                                                       "date": album_date.date(),
                                                       "owner": owner,
                                                       "description": "Blaba"
                                                   })
            album.save()
            albums.append(album)
        return albums

    def get_photos_and_thumbnail(self, album, photo_data, cache_data):
        """ Return a tuple with album object, photo and thumbnail"""
        album_year = datetime.strftime(album.date, "%Y")
        photo_year_data = photo_data.get(album_year)
        thumbnail_year_data = cache_data.get(album_year)
        if photo_year_data is not None:
            photos = photo_year_data.get(album.name).get('files')

        if thumbnail_year_data is not None:
            thumbnails = thumbnail_year_data.get(album.name).get('files')

        return [(album, photo, "caches/{}/{}/{}".format(album.date.year, album.name, thumbnail))
                for photo, thumbnail in zip(photos, thumbnails)]
