from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from gallery.models import Album
from gallery.serializers.serializers import AlbumSerializer


class GalleryCommonMixin(object):
    """Provide can_view_all() and show_public() utility methods."""
    allow_future = True

    def can_view_all(self):
        if not hasattr(self, '_can_view_all'):
            self._can_view_all = self.request.user.has_perm('gallery.view')
        return self._can_view_all

    def show_public(self):
        session = self.request.session
        if not hasattr(self, '_show_public'):
            if self.request.user.is_authenticated and not self.can_view_all():
                if 'show_public' in self.request.GET:
                    self._show_public = session['show_public'] = True
                elif 'hide_public' in self.request.GET:
                    self._show_public = session['show_public'] = False
                else:
                    self._show_public = session.setdefault('show_public', False)
            else:
                self._show_public = True
        return self._show_public


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


class GalleryIndexView(GalleryCommonMixin, AlbumListMixin, ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(GalleryIndexView, self).get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            qs = qs.filter(name__contains=query)
        return qs


class AlbumView(GalleryCommonMixin, AlbumListMixin, ModelViewSet):
    model = Album
    serializer_class = AlbumSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, *args, **kwargs):
        album = self.get_object()
        serializer = self.get_serializer(album)
        return Response(serializer.data)
