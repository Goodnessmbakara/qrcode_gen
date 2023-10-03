from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QRCodeDataViewSet

router = DefaultRouter()
router.register(r'', QRCodeDataViewSet)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)