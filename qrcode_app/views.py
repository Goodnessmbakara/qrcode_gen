from rest_framework import viewsets
from .models import QRCodeData
from django.urls import reverse
from .serializers import QRCodeDataSerializer
import qrcode

from django.core.files import File


from django.conf import settings
import os

from rest_framework import status
from rest_framework.response import Response

class QRCodeDataViewSet(viewsets.ModelViewSet):
    queryset = QRCodeData.objects.all()
    serializer_class = QRCodeDataSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(instance.data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Define the directory path where QR code images will be saved
        save_directory = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        
        img_path = os.path.join(save_directory, f"{instance.id}.png")
        img.save(img_path)
        
        # Open the saved image file
        with open(img_path, 'rb') as img_file:
            instance.qr_code.save(f"{instance.id}.png", File(img_file), save=True)
        
        # Get the URL for the saved QR code image
        img_url = self.request.build_absolute_uri(instance.qr_code.url.lstrip('/'))
        
        # Include the image URL in the response
        response_data = {
            'id': instance.id,
            'data': instance.data,
            'qr_code_url': img_url,
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)

