import hashlib

from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import get_objects_for_user, assign_perm
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.models.photo import Photo
from gallery.serializers.serializers import PhotoSerializer
from gallery.utils import s3_manager
from photogallery import settings


class PhotoView(PermissionRequiredMixin,
                GenericViewSet):
    model = Album
    queryset = Album.objects
    serializer_class = PhotoSerializer
    lookup_field = "id"

    permission_classes = [IsAuthenticated]
    permission_required = "view_album"
    return_403 = True

    @action(methods=['get'],
            detail=False,
            url_path='album/(?P<id>\d+)',
            url_name="get_photos_by_album")
    def get_photos(self, request, id):
        album = self.get_object()
        photo_qs = get_objects_for_user(request.user, 'gallery.view_photo')
        photo_qs = photo_qs.filter(album__id=album.id)
        serializer = self.get_serializer(photo_qs, many=True)
        return Response(serializer.data)


class PhotoCreateView(PermissionRequiredMixin,
                      GenericViewSet):
    model = Album
    queryset = Album.objects
    lookup_field = "id"

    permission_classes = [IsAuthenticated]
    permission_required = "add_photos"
    return_403 = 403

    @action(methods=['post'],
            detail=False,
            url_path='sign/album/(?P<id>\d+)',
            url_name='photo-sign')
    def sign(self, request, id):
        album = self.get_object()
        photo_filename = request.data.get('filename')
        if photo_filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'reason': 'photo filename not found'},
                            content_type='application/json')

        photo_file_path = "photos/{}/{}".format(album.folder_path, photo_filename)

        hsh = hashlib.sha256()
        hsh.update(str(settings.SECRET_KEY).encode())
        hsh.update(str(album.id).encode())
        hsh.update(str(photo_filename).encode())

        thumbnail_filename = "{}{}".format(hsh.hexdigest()[:8], photo_filename[photo_filename.index('.'):])
        thumbnail_file_path = "cache/{}/{}".format(album.date.strftime('%d%m'), thumbnail_filename)
        response_data = dict()
        response_data['photo_url'] = s3_manager.get_put_signed_url(photo_file_path)
        response_data['thumbnail_filename'] = thumbnail_filename
        response_data['thumbnail_url'] = s3_manager.get_put_signed_url(thumbnail_file_path)

        return Response(status=status.HTTP_200_OK,
                        data=response_data,
                        content_type='application/json')

    @action(methods=['post'],
            detail=False,
            url_path='album/(?P<id>\d+)',
            url_name="add_photo")
    def add_photo(self, request, id):
        album = self.get_object()
        photo_filename = request.data.get('filename')
        thumbnail_filename = request.data.get('thumbnail')
        if photo_filename is None or thumbnail_filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'reason', 'Either photo filename or thumbnail is missing'},
                            content_type='application/json')

        photo, _ = Photo.objects.get_or_create(album=album,
                                               filename=photo_filename,
                                               defaults={
                                                   'thumbnail_file': thumbnail_filename
                                               })

        assign_perm('view_photo', self.request.user, photo)
        return Response(status=status.HTTP_200_OK)


class PhotoDeleteView(mixins.DestroyModelMixin,
                      GenericViewSet):
    model = Photo
    queryset = Photo.objects

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        photo = self.get_object()
        if request.user.has_perm('delete_photos', photo.album):
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={'reason':'User is not allowed to delete photo from this album'},
                        content_type='application/json')
