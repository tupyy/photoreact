from guardian.mixins import PermissionRequiredMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.serializers.serializers import AlbumSerializer


class AlbumFavoriteView(PermissionRequiredMixin,
                        GenericViewSet):
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'
    return_403 = True

    @action(methods=['post', 'delete'],
            detail=True,
            url_path="favorites",
            url_name='change-favorites')
    def change_favorites(self, request, id):
        self.check_permissions(request)
        album = self.get_object()
        if request.method == 'POST':
            album.favorites.add(request.user)
        else:
            album.favorites.remove(request.user)
        return Response(status=status.HTTP_200_OK)