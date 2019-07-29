from django.contrib.auth.models import User
from django.db import models

from src.python.gallery.models import Album


class UserFavorites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    album = models.ManyToManyField(Album, on_delete=models.CASCADE)
