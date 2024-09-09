import os
import uuid
from datetime import datetime

import qrcode
from django.conf import settings
from django.core.files import File
from django.shortcuts import redirect, render
from django.views import View

from .forms import QRCodeDataForm
from .models import QRCodeData


def generate_qr(request):
    if request.method == 'POST':
        form = QRCodeDataForm(request.POST)
        if not form.is_valid():
            return render(request, 'index.html', {'form': form})  # Show errors in the form if validation fails
        
        data = form.cleaned_data['qr_data']
        if not (data.startswith('http://') or data.startswith('https://')):
            data = 'https://' + data  # Ensuring URL starts with http:// or https://

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code as an image file
        unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex}.png"
        save_directory = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(save_directory, exist_ok=True)
        
        img_path = os.path.join(save_directory, unique_name)
        img.save(img_path)

        # Wrap the saved image in a Django File to be saved in a model
        with open(img_path, 'rb') as img_file:
            django_file = File(img_file)
            # Assuming your model has a FileField or ImageField named 'qr_code'
            instance = QRCodeData.objects.create(qr_data=data)
            instance.qr_code.save(unique_name, django_file, save=True)
        
        return redirect('display_qr', qr_code_name=unique_name)
    else:
        form = QRCodeDataForm()

    return render(request, 'index.html', {'form': form})

def index(request):
    if request.method == "POST":
        # Get data from the form
        data = request.POST.get("qr_data", None)
        
        if data:
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            response = HttpResponse(buffer, content_type="image/png")
            return response
        else:
            return render(request, "index.html", {"error": "Please enter valid data."})
    
    return render(request, "index.html")



def display_qr(request, qr_code_name):
    img_url = os.path.join(settings.MEDIA_URL, 'qrcodes', qr_code_name)
    return render(request, 'qrcode_image.html', {
        'img_url': img_url,
        'qr_code_name': qr_code_name  # Optional, for downloading the QR code with a specific name
    })


# View to download QR code (optional, can be linked to QR code image generation)
def download_qr_code(request, data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="qr_code.png"'
    return response

# View for the about page
def about(request):
    return render(request, "about.html")