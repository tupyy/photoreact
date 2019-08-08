import os

from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from gallery.models.album import Album


class Media(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, verbose_name="file name")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

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


class Video(Media):
    class Meta:
        default_permissions = (
            ('view_video', 'View video'),
            ('delete_video', 'Delete video')
        )


class Photo(Media):
    thumbnail_file = models.CharField(max_length=100, verbose_name="thumbnail_name")

    class Meta:
        default_permissions = (
            ('view_photo', 'View photo'),
            ('delete_photo', 'Delete photo')
        )

    def image_name(self):
        return os.path.join(self.album.folder_name, self.filename)

