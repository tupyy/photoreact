import os

from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from gallery.models.album import Album


class MediaManager(models.Manager):

    def allowed_for_user(self, user):
        media_cond = Q(access_policy__public=True)
        inherit = Q(album__access_policy__inherit=True)
        album_cond = Q(album__access_policy__public=True)
        if user.is_authenticated:
            media_cond |= Q(access_policy__users=user)
            media_cond |= Q(access_policy__groups__user=user)
            album_cond |= Q(album__access_policy__users=user)
            album_cond |= Q(album__access_policy__groups__user=user)
        return self.filter(media_cond | (inherit & album_cond)).distinct()


class Media(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, verbose_name="file name")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = MediaManager()

    class Meta:
        ordering = ('date', 'filename')
        default_permissions = ('add', 'change', 'delete')
        unique_together = ('album', 'filename')
        verbose_name = "media"
        verbose_name_plural = "medias"

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('gallery:media', args=[self.pk])

    @property
    def display_name(self):
        return self.date or os.path.splitext(self.filename)[0]


class Photo(Media):
    thumbnail = models.CharField(max_length=100, verbose_name="thumbnail_name")

    def image_name(self):
        return os.path.join(self.album.dirpath, self.filename)

