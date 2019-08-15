from django.contrib.auth.models import User
from django.db import models

from gallery.models.album import Album


class AlbumUserFavorites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    album = models.ManyToManyField(Album)

    def __str__(self):
        return self.user.__str__() + ' ' + self.album.__str__()