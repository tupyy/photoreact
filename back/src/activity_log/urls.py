from __future__ import unicode_literals

from rest_framework import routers
from activity_log.views import ActivityLogView

router = routers.SimpleRouter()
router.register(r'api/activity', ActivityLogView, basename='activity')
urlpatterns = router.urls
