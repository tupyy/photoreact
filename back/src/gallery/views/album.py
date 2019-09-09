from collections import Iterable

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from guardian.mixins import PermissionListMixin
from permissions.mixins import PermissionRequiredMixin
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from gallery.filters import AlbumFilter
from gallery.models.album import Album
from gallery.models.category import Category, Tag
from gallery.serializers.serializers import AlbumSerializer, CategorySerializer, TagSerializer


class OrderingMixin(object):

    def get_ordering(self, qs):
        order_fields = self.request.GET.getlist('ordering')
        if len(order_fields) == 0:
            return qs
        for order_field in order_fields:
            if self.is_field(order_field):
                qs = qs.order_by(order_field)
        return qs

    def is_field(self, field_name):
        all_fields = Album._meta.get_fields()
        return field_name in [field.name for field in all_fields]


class AlbumListView(PermissionListMixin,
                    OrderingMixin,
                    ListAPIView,
                    GenericViewSet):
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = 'id'

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AlbumFilter

    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'

    def list(self, request, *args, **kwargs):
        qs = self.get_ordering(self.filter_queryset(self.get_queryset()))

        limit = self.request.query_params.get('limit', None)
        try:
            if limit is not None:
                qs = qs.all()[:int(limit)]
        except ValueError:
            pass

        serializer = self.get_serializer(qs, many=True)
        data = dict()
        data['size'] = qs.count()
        data['albums'] = serializer.data
        return Response(data)

    def post(self, request):
        from gallery.utils.validate_data import validate_list
        ids = validate_list(request.data.get('ids'), int)
        if len(ids) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'list of IDs missing or is corrupted'},
                            content_type='application/json')
        qs = self.get_queryset().filter(pk__in=ids)
        serializer = self.get_serializer(qs, many=True)
        data = dict()
        data['size'] = qs.count()
        data['albums'] = serializer.data
        return Response(data)

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
        data = dict()
        data['size'] = qs.count()
        data['albums'] = serializer.data
        return Response(data)


class AlbumView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    model = Album
    queryset = Album.objects
    serializer_class = AlbumSerializer
    lookup_field = "id"

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

    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'
    raise_exception = True

    @action(methods=['get'],
            detail=True,
            url_path='categories',
            url_name='get_categories')
    def get_categories(self, request, id=None):
        self.check_permissions(request)
        instance = self.get_object()
        categories_qs = instance.categories.all()
        categories_serializer = CategorySerializer(categories_qs, many=True)
        data = {"id": id,
                "categories": categories_serializer.data}
        return Response(status=status.HTTP_200_OK, data=data)

    @action(methods=['post'],
            detail=True,
            url_path='category',
            url_name='add_category')
    def add_category(self, request, id=None):
        self.check_permissions(request)
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

    permission_classes = [IsAuthenticated]
    permission_required = 'view_album'
    raise_exception = True

    @action(methods=['get'],
            detail=True,
            url_path='tags',
            url_name='get_tags')
    def get_tags(self, request, id=None):
        self.check_permissions(request)
        instance = self.get_object()
        tags_qs = instance.tags.all()
        tags_serializer = TagSerializer(tags_qs, many=True)
        data = {"id": id,
                "tags": tags_serializer.data}
        return Response(status=status.HTTP_200_OK, data=data)

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
