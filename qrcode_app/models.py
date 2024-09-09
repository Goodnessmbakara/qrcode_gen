from django.db import models
# from rest_framework_api_key.models import AbstractAPIKey

# class IPAddressAPIKey(AbstractAPIKey):
#     ip_address = models.GenericIPAddressField()

#     class Meta(AbstractAPIKey.Meta):
#         verbose_name = "IP Address API key"
#         verbose_name_plural = "IP Address API keys"

class QRCodeData(models.Model):
    qr_data = models.TextField()
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return self.data
