from gallery.models import Album


class AlbumListMixin(object):
    """Perform access control and database optimization for albums."""
    model = Album
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super(AlbumListMixin, self).get_context_data(**kwargs)
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


