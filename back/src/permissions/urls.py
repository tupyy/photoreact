from __future__ import unicode_literals

from rest_framework import routers

import permissions.views

router = routers.SimpleRouter()
router.register(r'api/permission', permissions.views.AlbumPermissionView, basename='permission')
router.register(r'api/permission/log', permissions.views.PermissionLogListView, basename='permission_logs')

urlpatterns = router.urls
