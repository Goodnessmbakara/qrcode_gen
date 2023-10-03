from django.db import models

class QRCodeData(models.Model):
    data = models.TextField()
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return self.data
