import os

from django.db import models
from django.shortcuts import reverse
from guardian.shortcuts import assign_perm

from gallery.models.album import Album


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, verbose_name="file name")
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    thumbnail_file = models.CharField(max_length=100, verbose_name="thumbnail_name")

    class Meta:
        ordering = ('date', 'filename')
        default_permissions = ('add', 'view', 'change', 'delete')
        unique_together = ('album', 'filename')
        verbose_name = "photo"
        verbose_name_plural = "photos"

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('gallery:photo', args=[self.pk])

    @property
    def display_name(self):
        return self.date or os.path.splitext(self.filename)[0]


class Video(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, verbose_name="file name")
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('date', 'filename')
        default_permissions = ('add', 'view', 'change', 'delete')
        unique_together = ('album', 'filename')
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('gallery:video', args=[self.pk])

    @property
    def display_name(self):
        return self.date or os.path.splitext(self.filename)[0]



