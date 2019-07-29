# coding: utf-8
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from src.python.gallery.models.category import Category, Tag


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
        return self.filter(album_cond).distinct()


@python_2_unicode_compatible
class Album(models.Model):
    category = models.ManyToManyField(Category, on_delete=models.CASCADE)
    dirpath = models.CharField(max_length=200, verbose_name="directory path")
    date = models.DateField()
    name = models.CharField(max_length=100, blank=True)
    owner = models.OneToOneField(User, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, on_delete=models.CASCADE)

    objects = AlbumManager()

    class Meta:
        ordering = ('date', 'name', 'dirpath', 'category')
        unique_together = ('dirpath', 'category')
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

    def get_next_in_queryset(self, albums):
        albums = albums.filter(
            Q(date__gt=self.date) |
            Q(date=self.date, name__gt=self.name) |
            Q(date=self.date, name=self.name, dirpath__gt=self.dirpath) |
            Q(date=self.date, name=self.name, dirpath=self.dirpath, category__gt=self.category))
        return albums.order_by('date', 'name', 'dirpath', 'category')[:1].get()

    def get_previous_in_queryset(self, albums):
        albums = albums.filter(
            Q(date__lt=self.date) |
            Q(date=self.date, name__lt=self.name) |
            Q(date=self.date, name=self.name, dirpath__lt=self.dirpath) |
            Q(date=self.date, name=self.name, dirpath=self.dirpath, category__lt=self.category))
        return albums.order_by('-date', '-name', '-dirpath', '-category')[:1].get()


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
