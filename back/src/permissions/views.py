from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from guardian.models import UserObjectPermission, GroupObjectPermission
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.serializers.serializers import AlbumSerializer
from permissions.mixins import IsOwner


class AlbumPermissionView(GenericViewSet):
    """ View to handle permissions APIs """
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

    permission_classes = [IsAuthenticated, IsOwner]

    @action(methods=['get', 'post', 'delete'],
            detail=True,
            url_path='permissions',
            url_name='get_permissions')
    def handle_object_permissions(self, request, id=None):
        instance = self.get_object()
        if request.method == 'GET':
            user_qs = UserObjectPermission.objects.filter(object_pk=instance.id) \
                .select_related("permission") \
                .select_related("user")
            groups_qs = GroupObjectPermission.objects.filter(object_pk=instance.id) \
                .select_related("permission") \
                .select_related("group")

            return Response(status=status.HTTP_200_OK,
                            data=[self.queryset_to_list(user_qs),
                                  self.queryset_to_list(groups_qs, is_group=True)],
                            content_type="application/json")
        else:
            data = self.remove_owner(instance.owner, request.data)
            for entry in data:
                user_or_group_model = {'user_id': User, 'group_id': Group}[
                    'user_id' if entry.get('user_id') else 'group_id']
                user_or_group = get_object_or_404(user_or_group_model,
                                                  pk=entry['user_id' if entry.get('user_id') else 'group_id'])
                permissions = entry.get('permissions')
                method = assign_perm if request.method == "POST" else remove_perm
                if permissions:
                    for permission in permissions:
                        method(permission, user_or_group, instance)

            return Response(status=status.HTTP_200_OK)

    def queryset_to_list(self, qs, is_group=False):
        """
            Return a list of list of dictionaries as following
            [
                [
                  {
                    "id": 1,
                    "username": "batman",
                    "permissions": [("Add photos", "add_photo"),"("View photos, view_photo")]
                  },
                  {
                    "id": 2,
                    "username": "superman",
                    "permissions": [("Add photos", "add_photo"),"("View photos, view_photo")]
                  }
                ],
                [
                    {
                        "id": 1,
                        "group_name": "batman_friends",
                        "permissions": [("Add photos", "add_photo"),"("View photos, view_photo")]
                    },
                ]
            ]
        """
        if not is_group:
            objects = [(p.user.id, p.user.username, p.permission.name, p.permission.codename) for p in qs.all()]
        else:
            objects = [(p.group.id, p.group.name, p.permission.name, p.permission.codename) for p in qs.all()]

        # set the key value for name field
        key_name_name = "username" if not is_group else "group_name"

        d = dict()
        for entry in objects:
            key = entry[1]
            if key in d:
                d[key]["permissions"].append((entry[2], entry[3]))
            else:
                d[key] = {
                    "id": entry[0],
                    key_name_name: entry[1],
                    "permissions": [(entry[2], entry[3])]
                }
        return [v for k, v in d.items()]

    def remove_owner(self, owner, data):
        """
        Changing permissions for owner(by the owner) is not allowed. So we remove any entry of owner from request.data
        before we proceed with any modification of permissions
        """
        for entry in data:
            pk = entry.get('user_id', -1)
            if pk == owner.id:
                data.remove(entry)
        return data