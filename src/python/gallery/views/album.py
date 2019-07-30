import random

from django.contrib.auth.models import User

from gallery.models import Album
from photogallery import settings


class AlbumListMixin(object):
    """Perform access control and database optimization for albums."""
    model = Album
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = dict()
        context['object_list'] = self.get_queryset()
        context['show_public'] = self.show_public()
        return context

    def get_queryset(self):
        if self.can_view_all():
            qs = Album.objects.all()
            qs = qs.prefetch_related('photo_set')
        else:
            qs = Album.objects.allowed_for_user(self.request.user, self.show_public())
            qs = qs.prefetch_related('access_policy__groups')
            qs = qs.prefetch_related('access_policy__users')
            qs = qs.prefetch_related('photo_set__access_policy__groups')
            qs = qs.prefetch_related('photo_set__access_policy__users')
        return qs.order_by('-date', '-name')


class AlbumListWithPreviewMixin(AlbumListMixin):
    """Compute preview lists for albums."""

    def get_context_data(self, **kwargs):
        context = super(AlbumListWithPreviewMixin, self).get_context_data(**kwargs)
        user = self.request.user
        if not self.can_view_all() and user.is_authenticated:
            # Avoid repeated queries - this is specific to django.contrib.auth
            user = User.objects.prefetch_related('groups').get(pk=user.pk)
        for album in context['object_list']:
            if self.can_view_all():
                photos = list(album.photo_set.all())
            else:
                photos = [
                    photo
                    for photo in album.photo_set.all()
                    if photo.is_allowed_for_user(user)
                ]
            album.photos_count = len(photos)
            preview_count = getattr(settings, 'GALLERY_PREVIEW_COUNT', 5)
            if len(photos) > preview_count:
                selection = sorted(random.sample(
                    range(album.photos_count), preview_count))
                album.preview = [photos[index] for index in selection]
            else:
                album.preview = list(photos)
        context['title'] = getattr(settings, 'GALLERY_TITLE', "Gallery")
        return context


