from rest_framework import serializers
from .models import QRCodeData


from django.conf import settings

class QRCodeDataSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()  # Custom field for QR code URL

    class Meta:
        model = QRCodeData
        fields = ['id', 'data', 'qr_code_url']

    def get_qr_code_url(self, obj):
        # Build the URL for the saved QR code image
        if obj.qr_code and hasattr(obj.qr_code, 'url'):
            img_url = self.context['request'].build_absolute_uri(obj.qr_code.url)
            return img_url
        else:
            return None



