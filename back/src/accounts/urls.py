from rest_framework.routers import SimpleRouter

from accounts.views import AccountUserView

router = SimpleRouter()
router.register(r'api/account', AccountUserView, basename="account")
urlpatterns = router.urls
