# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from gallery.utils.s3_manager import get_signed_url


class AlbumManager(models.Manager):

    def allowed_for_user(self, user, include_public=True):
        album_cond = Q()
        if include_public:
            album_cond |= Q(access_policy__public=True)
        if user.is_authenticated:
            album_cond |= Q(access_policy__users=user)
            album_cond |= Q(access_policy__groups__user=user)
            album_cond |= Q(owner__exact=user)
        return self.filter(album_cond).distinct()

    def allow_only_for_owner(self, user):
        album_cond = Q()
        if user.is_authenticated:
            album_cond |= Q(owner__exact=user)
        return self.filter(album_cond).distinct()


@python_2_unicode_compatible
class Album(models.Model):
    dirpath = models.CharField(max_length=200, verbose_name="directory path")
    date = models.DateField(verbose_name="creation_date")
    name = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('date', 'name', 'dirpath')
        unique_together = ('dirpath',)
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
            return get_signed_url(photo[0].thumbnail)
        return ""

    def __str__(self):
        return self.dirpath

    def get_absolute_url(self):
        return reverse('gallery:album', args=[self.pk])

    @property
    def display_name(self):
        return self.name or self.dirpath.replace('/', ' > ')

    def is_allowed_for_user(self, user):
        access_policy = self.get_access_policy()
        return access_policy is not None and access_policy.allows(user)

    def is_owner(self, user):
        return self.owner.id == user.id
