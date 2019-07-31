from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from gallery.models import Photo
from gallery.serializers.serializers import PhotoSerializer
from gallery.views.album import GalleryCommonMixin


class PhotoView(GalleryCommonMixin, GenericAPIView, ViewSet):
    model = Photo
    serializer_class = PhotoSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.can_view_all():
            qs = Photo.objects.all()
        else:
            qs = Photo.objects.allowed_for_user(self.request.user)
        return qs.select_related('album')

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        if self.can_view_all():
            qs = queryset.album.photo_set.all()
        else:
            qs = queryset.album.photo_set.allowed_for_user(self.request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)