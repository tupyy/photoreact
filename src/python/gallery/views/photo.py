import hashlib

from django.shortcuts import get_object_or_404
from guardian.decorators import permission_required
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.serializers.serializers import PhotoSerializer
from gallery.utils import s3_manager
from photogallery import settings


class PhotoView(GenericViewSet):
    serializer_class = PhotoSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['get'],
            detail=False,
            url_path='album/(?P<id>\d+)',
            url_name="get_photos_by_album")
    def get_photos(self, request, id):
        album = get_object_or_404(Album, pk=id)

        if not request.user.has_perm('view_album', album):
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"reason": "User not allowed to view the album"},
                            content_type="application/json")

        photo_qs = get_objects_for_user(request.user, 'gallery.view_photo')
        photo_qs = photo_qs.filter(album__id=album.id)
        serializer = self.get_serializer(photo_qs, many=True)
        return Response(serializer.data)

    @action(methods=['post'],
            detail=False,
            url_path='sign/album/(?P<id>\d+)',
            url_name='photo-sign')
    def sign(self, request, id):
        album = get_object_or_404(Album, pk=id)

        if not request.user.has_perm('add_photos', album):
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={'reason': 'User not allowed to upload photos'},
                            content_type='application/json')

        photo_filename = request.data.get('filename')
        if photo_filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'reason':'photo filename not found'},
                            content_type='application/json')

        photo_file_path = "photos/{}/{}".format(album.folder_path, photo_filename)

        hsh = hashlib.md5()
        hsh.update(str(settings.SECRET_KEY).encode())
        hsh.update(str(album.id).encode())
        hsh.update(str(request.data.get('filename')).encode())

        thumbnail_filename = "{}{}".format(hsh.hexdigest()[:8], photo_filename[photo_filename.index('.'):])
        thumbnail_file_path = "cache/{}/{}".format(album.date.strftime('%d%m'), thumbnail_filename)
        response_data = dict()
        response_data['photo_url'] = s3_manager.get_put_signed_url(photo_file_path)
        response_data['thumbnail_filename'] = thumbnail_filename
        response_data['thumbnail_url'] = s3_manager.get_put_signed_url(thumbnail_file_path)

        return Response(status=status.HTTP_200_OK,
                        data=response_data,
                        content_type='application/json')
