from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer


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
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

