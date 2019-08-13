from collections import Iterable
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin
from guardian.models import UserObjectPermission, GroupObjectPermission
from rest_framework import status, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.models.album import Album
from gallery.models.category import Category, Tag
from gallery.permissions.owner_permission import IsOwner
from gallery.serializers.serializers import AlbumSerializer, CategorySerializer, TagSerializer


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


class AlbumCategoryView(PermissionRequiredMixin,
                        GenericViewSet):
    """ View to handle all category API """
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'
    raise_exception = True

    @action(methods=['get'],
            detail=True,
            url_path='categories',
            url_name='get_categories')
    def get_categories(self, request, id=None):
        instance = self.get_object()
        categories_qs = instance.categories.all()
        categories = CategorySerializer(categories_qs, many=True)
        return Response(status=status.HTTP_200_OK, data=categories.data)

    @action(methods=['post'],
            detail=True,
            url_path='category',
            url_name='add_category')
    def add_category(self, request, id=None):
        instance = self.get_object()
        if not request.user.has_perm('change_album', instance):
            return Response(status=status.HTTP_403_FORBIDDEN)

        category_names = request.data
        if isinstance(category_names, str):
            category = Category.objects.filter(name__exact=category_names)
            instance.categories.add(category)
        elif isinstance(category_names, Iterable):
            categories = Category.objects.filter(name__in=category_names)
            instance.categories.add(*categories.all())
        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete', 'put'],
            detail=True,
            url_path='category/(?P<category_id>\w+)',
            url_name='delete_category')
    def delete_category(self, request, id, category_id):
        instance = self.get_object()
        if not request.user.has_perm('change_album', instance):
            return Response(status=status.HTTP_403_FORBIDDEN)

        category = instance.categories.get(pk=category_id)
        if category is not None:
            instance.categories.remove(Category.objects.get(pk=category_id))
            if request.method == 'DELETE':
                return Response(status=status.HTTP_200_OK,
                                data={'category': category_id},
                                content_type="application/json")
            else:
                new_category = get_object_or_404(Category, pk=request.data.get('category_id'))
                instance.categories.add(new_category)
                return Response(status=status.HTTP_200_OK,
                                data={'category': new_category.id},
                                content_type='application/json')
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'reason': 'Category not found'},
                        content_type='application/json')


class AlbumTagView(PermissionRequiredMixin,
                   GenericViewSet):
    """ View to handle all category API """
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'
    raise_exception = True

    @action(methods=['get'],
            detail=True,
            url_path='tags',
            url_name='get_tags')
    def get_tags(self, request, id=None):
        instance = self.get_object()
        tags_qs = instance.tags.all()
        tags = TagSerializer(tags_qs, many=True)
        return Response(status=status.HTTP_200_OK, data=tags.data)

    @action(methods=['post'],
            detail=True,
            url_path='tag',
            url_name='add_tag')
    def add_tag(self, request, id=None):
        """ same as category but we create tags if they don't exist """
        instance = self.get_object()
        if not request.user.has_perm('change_album', instance):
            return Response(status=status.HTTP_403_FORBIDDEN)

        tag_names = request.data
        if isinstance(tag_names, str):
            # get or create tag
            tag, _ = Tag.objects.get_or_create(name=tag_names)
            instance.tags.add(tag)
        elif isinstance(tag_names, Iterable):
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete', 'put'],
            detail=True,
            url_path='tag/(?P<tag_id>\w+)',
            url_name='delete_tag')
    def delete_tag(self, request, id, tag_id):
        instance = self.get_object()
        if not request.user.has_perm('change_album', instance):
            return Response(status=status.HTTP_403_FORBIDDEN)

        tag = instance.tags.get(pk=tag_id)
        if tag is not None:
            instance.tags.remove(Tag.objects.get(pk=tag_id))
            if request.method == 'DELETE':
                return Response(status=status.HTTP_200_OK,
                                data={'tag_id': tag_id},
                                content_type="application/json")
            else:
                new_tag, _ = Tag.objects.get_or_create(name=request.data.get('tag_name'))
                instance.tags.add(new_tag)
                return Response(status=status.HTTP_200_OK,
                                data={'category': new_tag.id},
                                content_type='application/json')
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'reason': 'Category not found'},
                        content_type='application/json')


class AlbumPermissionView(GenericViewSet):
    """ View to handle permissions APIs """
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    @action(methods=['get'],
            detail=True,
            url_path='permissions',
            url_name='get_permissions')
    def get_object_permissions(self, request, id=None):
        instance = self.get_object()
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
