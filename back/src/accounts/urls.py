from rest_framework.routers import SimpleRouter

from accounts.views import AccountUserView

router = SimpleRouter()
router.register(r'accounts', AccountUserView, basename="accounts")
urlpatterns = router.urls
