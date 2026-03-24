from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import QRCode


def home(request):
    return HttpResponse(
        "<h1>ScanBack QR System</h1>"
        "<p><a href='/admin/'>Admin Panel</a></p>"
        "<p>QR kodlarni admin panelda yarating.</p>"
    )


def public_page(request, slug):
    qr = get_object_or_404(QRCode, slug=slug)
    phone_link = qr.get_tel_link()
    return render(request, "qrhub/public.html", {"qr": qr, "phone_link": phone_link})
