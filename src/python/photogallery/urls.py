"""app URL Configuration
"""

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from gallery.urls import urlpatterns as gallery_url

# Authentication
authentication_urls = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += authentication_urls
urlpatterns += gallery_url
