from django.shortcuts import get_object_or_404
from guardian.mixins import PermissionListMixin
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.serializers.serializers import PhotoSerializer


class PhotoView(PermissionListMixin,
                GenericViewSet):
    serializer_class = PhotoSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = "view_photo"

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
