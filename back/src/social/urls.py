from rest_framework import routers

from social import views as social_views

router = routers.SimpleRouter()
router.register(r'favorites', social_views.AlbumFavoriteView, base_name='favorites')
urlpatterns = router.urls
