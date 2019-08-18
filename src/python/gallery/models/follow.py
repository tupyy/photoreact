from django.contrib.auth.models import User
from django.db import models

from gallery.models.album import Album


class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "followed user"
        verbose_name_plural = "followed users"

    def __str__(self):
        return '{}_following_{}'.format(self.user.username,
                                        self.followed_user.username)


class FollowAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "followed album"
        verbose_name_plural = "followed albums"

    def __str__(self):
        return "{}_follows_album_{}".format(self.user.username,
                                            self.album.id)
