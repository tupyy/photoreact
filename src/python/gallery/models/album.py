# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from guardian.shortcuts import assign_perm

from gallery.models.category import Category, Tag
from gallery.utils.s3_manager import get_get_signed_url


class AlbumManager(models.Manager):

    def create(self, *args, **kwargs):
        album = super().create(*args, **kwargs)

        # Assign all permissions to owner
        assign_perm('add_photos', kwargs['owner'], album)
        assign_perm('change_album', kwargs['owner'], album)
        assign_perm('delete_album', kwargs['owner'], album)
        assign_perm('add_permissions', kwargs['owner'], album)
        assign_perm('change_permissions', kwargs['owner'], album)
        assign_perm('delete_permissions', kwargs['owner'], album)

        return album


@python_2_unicode_compatible
class Album(models.Model):
    folder_path = models.CharField(max_length=200, verbose_name="directory path")
    date = models.DateField(verbose_name="creation_date")
    name = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    favorites = models.ManyToManyField(User, blank=True, related_name="favorites")

    objects = AlbumManager()

    def is_favorites(self, user):
        return self.favorites.values_list('username').filter(username__exact=user.username).count() > 0

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
        photo = self.photo_set.all()
        if photo.count() > 0:
            return get_get_signed_url(photo[0].thumbnail_file)
        return ""

    def __str__(self):
        return self.folder_path

    def get_absolute_url(self):
        return reverse('gallery:album', args=[self.pk])

    @property
    def display_name(self):
        return self.name or self.folder_path.replace('/', ' > ')
