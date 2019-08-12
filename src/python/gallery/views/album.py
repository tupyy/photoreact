from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from guardian.mixins import PermissionListMixin
from rest_framework import status, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.serializers.serializers import AlbumSerializer


class AlbumFilterListMixin(object):

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.filter_by_name(qs)
        qs = self.filter_by_period(qs)
        return qs

    def filter_by_name(self, qs):
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            qs = qs.filter(owner__id=owner)
        return qs

    def filter_by_period(self, qs):
        start_date_str = self.request.query_params.get('start', None)
        end_date_str = self.request.query_params.get('end', None)

        if (start_date_str and end_date_str) is not None:
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
            date_cond = Q(date__gte=start_date)
            date_cond &= Q(date__lte=end_date)
            qs = qs.filter(date_cond)
        return qs


class AlbumListView(AlbumFilterListMixin,
                    PermissionListMixin,
                    ListAPIView,
                    GenericViewSet):
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = 'id'

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'],
            detail=False,
            url_path='owner/(?P<pk>\d+)',
            url_name='get_by_user')
    def get_albums_by_user(self, request, pk):
        user = User.objects.get(pk=pk)
        if user is None:
            return Response(data={'reason': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        qs = self.get_queryset().filter(owner__username__exact=user.username)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class AlbumView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.has_perm('gallery.add_album'):
            request.data['owner'] = request.user.username
            return super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, *args, **kwargs):
        album = self.get_object()
        if self.request.user.has_perm('view_album', album):
            serializer = self.get_serializer(album)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.has_perm('change_album', instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.has_perm('delete_album', instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
