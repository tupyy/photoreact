from __future__ import unicode_literals

from rest_framework import routers

import permissions.views

router = routers.SimpleRouter()
router.register(r'api/permission', permissions.views.AlbumPermissionView, basename='permission')

urlpatterns = router.urls
