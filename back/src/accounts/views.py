import hashlib

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from gallery.utils import s3_manager

from photogallery.settings import STATIC_PROFILE_PHOTO_URL, SECRET_KEY


class AccountUserView(GenericViewSet):
    model = UserProfile
    queryset = UserProfile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj = self.queryset.filter(user__username__exact=user.username).first()
        return obj

    @action(methods=['get', 'put'],
            detail=False,
            url_path='profile',
            url_name="get_profile")
    def get_profile(self, request):
        obj = self.get_object()
        if request.method == 'GET':
            serializer = self.get_serializer(obj)
            return Response(status=status.HTTP_200_OK, data=serializer.data, content_type="application/json")
        else:
            serializer = self.get_serializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data, content_type="application/json")
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"reason": serializer.errors},
                            content_type="application/json")

    @action(methods=['post'],
            detail=False,
            url_path='photo/sign',
            url_name='photo-sign')
    def sign(self, request):
        photo_filename = request.data.get('filename')
        if photo_filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'reason': 'photo filename not found'},
                            content_type='application/json')

        photo_file_path = STATIC_PROFILE_PHOTO_URL + photo_filename
        response_data = dict()
        response_data['filepath'] = photo_file_path
        response_data['url'] = s3_manager.get_put_signed_url(photo_file_path)

        return Response(status=status.HTTP_200_OK,
                        data=response_data,
                        content_type='application/json')

    @action(methods=['post'],
            detail=False,
            url_path='photo',
            url_name="save-photo")
    def save_photo(self, request):
        profile = self.get_object()
        photo_filename = request.data.get('filename')
        if photo_filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'reason', 'Photo filename is missing.'},
                            content_type='application/json')
        profile.photo = photo_filename
        profile.save()
        return Response(status=status.HTTP_200_OK)
