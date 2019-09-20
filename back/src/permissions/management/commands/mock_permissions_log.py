import itertools
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission

from gallery.models.album import Album
from permissions.models import PermissionLog


class Command(BaseCommand):
    permissions = ['add_photos', 'change_album', 'delete_album', 'view_album']
    operation = [('add', 'add'), ('delete', 'delete'), ('modify', 'modify')]

    def handle(self, *args, **options):
        user_from = User.objects.filter(username__exact='cosmin').first()
        others = User.objects.all().exclude(username__iexact='cosmin')
        albums = Album.objects.all()
        groups = Group.objects.all()

        for user in itertools.chain(others, groups):
            for i in range(3):
                permission_name = self.permissions[random.randint(0, 3)]
                permission = Permission.objects.filter(codename__exact=permission_name).first()
                _operation = self.operation[random.randint(0, 2)]
                album = albums[random.randint(0, len(albums))]
                if permission is not None:
                    permission_log = PermissionLog(user_from=user_from,
                                                   content_object=user,
                                                   album=album,
                                                   permission=permission,
                                                   operation=_operation[0])
                    permission_log.save()
