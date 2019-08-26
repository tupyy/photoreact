# coding: utf-8

from __future__ import unicode_literals

from rest_framework import routers

from gallery import views as gallery_views

app_name = 'gallery'

router = routers.SimpleRouter()
router.register(r'albums', gallery_views.AlbumListView, basename='albums')

router.register(r'album', gallery_views.AlbumCategoryView, basename='album')
router.register(r'album', gallery_views.AlbumView, basename='album')
router.register(r'album', gallery_views.AlbumTagView, basename='album')
router.register(r'album', gallery_views.AlbumPermissionView, basename='album')
router.register(r'album', gallery_views.AlbumFavoriteView, basename='album')

router.register(r'photos', gallery_views.PhotoView, basename='photos')
router.register(r'photo', gallery_views.PhotoCreateView, basename='photo')
router.register(r'photo', gallery_views.PhotoDeleteView, basename='photo')

router.register(r'activities', gallery_views.ActivityLogView, basename='activities')
urlpatterns = router.urls
