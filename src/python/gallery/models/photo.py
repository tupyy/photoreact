# coding: utf-8

from __future__ import unicode_literals

import hashlib
import os

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from gallery.models.album import Album, AlbumAccessPolicy, AccessPolicy
from gallery.utils.storages import get_storage
from gallery.utils.s3_manager import get_signed_url, put_signed_url


class PhotoManager(models.Manager):

    def allowed_for_user(self, user):
        photo_cond = Q(access_policy__public=True)
        inherit = Q(album__access_policy__inherit=True)
        album_cond = Q(album__access_policy__public=True)
        if user.is_authenticated:
            photo_cond |= Q(access_policy__users=user)
            photo_cond |= Q(access_policy__groups__user=user)
            album_cond |= Q(album__access_policy__users=user)
            album_cond |= Q(album__access_policy__groups__user=user)
        return self.filter(photo_cond | (inherit & album_cond)).distinct()


@python_2_unicode_compatible
class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, verbose_name="file name")
    date = models.DateTimeField(null=True, blank=True)

    objects = PhotoManager()

    def get_signed_url(self):
        return get_signed_url(self.filename, self.filename[self.filename.index('.')+1:])

    def put_signed_url(self):
        return put_signed_url(self.filename, self.filename[self.filename.index('.')+1:])

    class Meta:
        ordering = ('date', 'filename')
        permissions = (
            ("view", "Can see all photos"),
            ("scan", "Can scan the photos directory"),
        )
        unique_together = ('album', 'filename')
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('gallery:photo', args=[self.pk])

    @property
    def display_name(self):
        return self.date or os.path.splitext(self.filename)[0]

    def get_effective_access_policy(self):
        try:
            return self.access_policy
        except PhotoAccessPolicy.DoesNotExist:
            pass
        try:
            album_access_policy = self.album.access_policy
        except AlbumAccessPolicy.DoesNotExist:
            pass
        else:
            if album_access_policy.inherit:
                return album_access_policy

    def is_allowed_for_user(self, user):
        access_policy = self.get_effective_access_policy()
        return access_policy is not None and access_policy.allows(user)

    # In the next two functions, images whose date is None may come
    # first or last, depending on the database.
    # These expressions are optimized for clarity, not concision.

    def get_next_in_queryset(self, photos):
        if self.date is None:
            photos = photos.filter(
                Q(date__isnull=False) |
                Q(date__isnull=True, filename__gt=self.filename))
        else:
            photos = photos.filter(
                Q(date__gt=self.date) |
                Q(date=self.date, filename__gt=self.filename))
        return photos.order_by('date', 'filename')[:1].get()

    def get_previous_in_queryset(self, photos):
        if self.date is None:
            photos = photos.filter(
                date__isnull=True, filename__lt=self.filename)
        else:
            photos = photos.filter(
                Q(date__isnull=True) |
                Q(date__lt=self.date) |
                Q(date=self.date, filename__gt=self.filename))
        return photos.order_by('-date', '-filename')[:1].get()

    def image_name(self):
        return os.path.join(self.album.dirpath, self.filename)


@python_2_unicode_compatible
class PhotoAccessPolicy(AccessPolicy):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='access_policy')

    class Meta:
        verbose_name = _("photo access policy")
        verbose_name_plural = _("photo access policies")

    def __str__(self):
        return "Access policy for %s" % self.photo
