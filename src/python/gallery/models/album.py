# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from gallery.utils.s3_manager import get_get_signed_url


@python_2_unicode_compatible
class Album(models.Model):
    folder_path = models.CharField(max_length=200, verbose_name="directory path")
    date = models.DateField(verbose_name="creation_date")
    name = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('date', 'name', 'folder_path')
        unique_together = ('folder_path',)
        verbose_name = "album"
        verbose_name_plural = "albums"
        default_permissions = ('add', 'change', 'delete', 'view')
        permissions = (
            ('add_photos', 'Add photos'),
            ('add_permissions', 'Add permissions'),
            ('change_permissions', 'Change permissions'),
            ('delete_permissions', 'Delete permissions'),
        )

    @property
    def preview(self):
        photo = self.photo_set.objects.filter(album_id__exact=self.id)
        if photo.count() > 0:
            return get_get_signed_url(photo[0].thumbnail)
        return ""

    def __str__(self):
        return self.folder_path

    def get_absolute_url(self):
        return reverse('gallery:album', args=[self.pk])

    @property
    def display_name(self):
        return self.name or self.folder_path.replace('/', ' > ')