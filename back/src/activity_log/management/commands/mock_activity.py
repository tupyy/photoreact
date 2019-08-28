import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from activity_log.models import ActivityLog
from gallery.models.album import Album


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()
        albums = Album.objects.all()

        for i in range(200):
            random_album = albums[random.randint(0, albums.count()-1)]
            random_user = users[random.randint(0, users.count()-1)]
            random_activity_type = ActivityLog.ACTIVITY_TYPE[random.randint(0, 3)]
            activity_log = ActivityLog(content_object=random_album,
                                       activity=random_activity_type[0],
                                       user=random_user)
            activity_log.save()
