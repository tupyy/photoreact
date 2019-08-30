from rest_framework import routers

from social import views as social_views

router = routers.SimpleRouter()
router.register(r'api/favorite', social_views.AlbumFavoriteView, base_name='favorite')
urlpatterns = router.urls
