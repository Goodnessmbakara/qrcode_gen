from django.views import View
from django.shortcuts import render, redirect
from .models import QRCodeData
from .forms import QRCodeDataForm
import qrcode
from django.core.files import File
from django.conf import settings
import os

from datetime import datetime
import uuid

class QRCodeDataView(View):
   def get(self, request):
       form = QRCodeDataForm()
       return render(request, 'qrcode_data_form.html', {'form': form})

   def post(self, request):
       form = QRCodeDataForm(request.POST)
       if form.is_valid():
           instance = form.save()
           unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex}.png"
           qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
           )
           qr.add_data(instance.data)
           qr.make(fit=True)
           img = qr.make_image(fill_color="black", back_color="white")

           save_directory = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
           os.makedirs(save_directory, exist_ok=True)
           os.chmod(save_directory, 0o755)

           img_path = os.path.join(save_directory, unique_name)
           img.save(img_path)

           with open(img_path, 'rb') as img_file:
               instance.qr_code.save(unique_name, File(img_file), save=True)

           img_url = request.build_absolute_uri(instance.qr_code.url.lstrip('/'))

           if not (instance.data.startswith('http://') or instance.data.startswith('https://')):
               # Prepend http:// to instance.data
               instance.data = 'https://' + instance.data

           return render(request, 'qrcode_image.html', {'img_url': img_url, 'data_url': instance.data, 'qr_code_name': unique_name })

       return render(request, 'qrcode_data_form.html', {'form': form})
