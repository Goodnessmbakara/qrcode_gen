from django.urls import path

from .views import QRCodeDataView



from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', QRCodeDataView.as_view(), name='qrcode_data'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)