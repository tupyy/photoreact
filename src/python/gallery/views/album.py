from datetime import datetime

from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from gallery.models import Album
from gallery.serializers.policy_serializers import AlbumAccessPolicySerializer
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


class AlbumFilterListMixin(object):

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.filter_by_name(qs)
        qs = self.filter_by_period(qs)
        qs = self.filter_by_category(qs)
        qs = self.filter_by_tag(qs)
        return qs

    def filter_by_name(self, qs):
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            qs = qs.filter(owner__id=owner)
        return qs

    def filter_by_period(self, qs):
        start_date_str = self.request.query_params.get('start_date', None)
        end_date_str = self.request.query_params.get('end_date', None)

        if (start_date_str and end_date_str) is not None:
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
            date_cond = Q(date__gte=start_date)
            date_cond &= Q(date__lte=end_date)
            qs = qs.filter(date_cond)
        return qs

    def filter_by_category(self, qs):
        categories_names = self.request.query_params.get('category')
        if categories_names is not None:
            if type(categories_names) is list:
                qs = qs.filter(categories__name__in=categories_names)
            else:
                qs = qs.filter(categories__name__in=[categories_names])
        return qs

    def filter_by_tag(self, qs):
        tag_names = self.request.query_params.get('tag')
        if tag_names is not None:
            if type(tag_names) is list:
                qs = qs.filter(tag__name__in=tag_names)
            else:
                qs = qs.filter(tag__name__in=[tag_names])
        return qs


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


class AlbumView(GalleryCommonMixin,
                AlbumFilterListMixin,
                AlbumListMixin,
                ModelViewSet):
    model = Album
    serializer_class = AlbumSerializer
    policies_serializer_class = AlbumAccessPolicySerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, *args, **kwargs):
        album = self.get_object()
        serializer = self.get_serializer(album)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """ Add a extra check. Only owner has the right to update the album """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.owner.id != self.request.user.id:
            return Response(status=404)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner.id != self.request.user.id:
            return Response(status=404)

        instance.photo_set.all().delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
