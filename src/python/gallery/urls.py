# coding: utf-8

from __future__ import unicode_literals

from django.conf.urls import url

from gallery import views as gallery_views
from rest_framework import routers

app_name = 'gallery'

router = routers.SimpleRouter()
router.register(r'album', gallery_views.AlbumView, basename='album')

urlpatterns = [
    url(r'^albums/$', gallery_views.album.AlbumListView.as_view(), name='albums-list'),
    url(r'^$', gallery_views.GalleryIndexView.as_view(), name='index'),
]

urlpatterns += router.urls
