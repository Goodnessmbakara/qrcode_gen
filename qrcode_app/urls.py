from django.urls import path

from .import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.QRCodeDataView.as_view(), name='qrcode_data'),
    path('', views.index, name='index'),  # Landing page with QR code generation
    path('about/', views.about, name='about'),  # About page
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('qr/<str:qr_code_name>/', views.display_qr, name='display_qr'),
    path('download/<str:data>/', views.download_qr_code, name='download_qr_code'),  # Download QR c
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)