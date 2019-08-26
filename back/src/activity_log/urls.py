from __future__ import unicode_literals

from rest_framework import routers
from activity_log.views import ActivityLogView

router = routers.SimpleRouter()
router.register(r'activities', ActivityLogView, basename='activities')
urlpatterns = router.urls
