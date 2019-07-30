# coding: utf-8
import os

from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from gallery.utils.s3_manager import get_signed_url, put_signed_url
from .category import Category, Tag


class AccessPolicy(models.Model):
    public = models.BooleanField(verbose_name="is public", default=False)
    groups = models.ManyToManyField(Group, blank=True, verbose_name="authorized groups")
    users = models.ManyToManyField(User, blank=True, verbose_name="authorized users")

    class Meta:
        abstract = True

    def allows(self, user):
        if self.public:
            return True
        if user.is_authenticated:
            if set(self.groups.all()) & set(user.groups.all()):
                return True
            if user in self.users.all():
                return True
        return False


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
    categories = models.ManyToManyField(Category, blank=True)
    dirpath = models.CharField(max_length=200, verbose_name="directory path")
    date = models.DateField()
    name = models.CharField(max_length=100, blank=True)
    owner = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = AlbumManager()

    @property
    def preview(self):
        photo = Photo.objects.filter(album__id__exact=self.id)
        if photo.count() > 0:
            return photo.get(0).get_signed_url()
        return ""

    class Meta:
        ordering = ('date', 'name', 'dirpath')
        unique_together = ('dirpath',)
        verbose_name = _("album")
        verbose_name_plural = _("albums")

    def __str__(self):
        return self.dirpath

    def get_absolute_url(self):
        return reverse('gallery:album', args=[self.pk])

    @property
    def display_name(self):
        return self.name or self.dirpath.replace('/', ' > ')

    def get_access_policy(self):
        try:
            return self.access_policy
        except AlbumAccessPolicy.DoesNotExist:
            pass

    def is_allowed_for_user(self, user):
        access_policy = self.get_access_policy()
        return access_policy is not None and access_policy.allows(user)


@python_2_unicode_compatible
class AlbumAccessPolicy(AccessPolicy):
    album = models.OneToOneField(Album, on_delete=models.CASCADE, related_name='access_policy')
    inherit = models.BooleanField(blank=True, default=True,
                                  verbose_name="photos inherit album access policy")

    class Meta:
        verbose_name = _("album access policy")
        verbose_name_plural = _("album access policies")

    def __str__(self):
        return "Access policy for %s" % self.album


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
        return get_signed_url(self.filename)

    def put_signed_url(self):
        return put_signed_url(self.filename)

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

