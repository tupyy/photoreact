from __future__ import unicode_literals

from rest_framework import routers

import permissions.views

router = routers.SimpleRouter()
router.register(r'permissions', permissions.views.AlbumPermissionView, basename='permissions')

urlpatterns = router.urls
