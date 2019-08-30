# coding: utf-8

from __future__ import unicode_literals

from rest_framework import routers

from gallery import views as gallery_views

app_name = 'gallery'

router = routers.SimpleRouter()
router.register(r'api/albums', gallery_views.AlbumListView, basename='albums')

router.register(r'api/album', gallery_views.AlbumCategoryView, basename='album')
router.register(r'api/album', gallery_views.AlbumView, basename='album')
router.register(r'api/album', gallery_views.AlbumTagView, basename='album')

router.register(r'api/photos', gallery_views.PhotoView, basename='photos')
router.register(r'api/photo', gallery_views.PhotoCreateView, basename='photo')
router.register(r'api/photo', gallery_views.PhotoDeleteView, basename='photo')

urlpatterns = router.urls
