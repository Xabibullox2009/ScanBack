from django.shortcuts import get_object_or_404, render

from .models import QRCode


def home(request):
    return render(request, "qrhub/home.html")


def public_qr(request, slug):
    qr_code = get_object_or_404(QRCode, slug=slug)
    return render(request, "qrhub/public.html", {"qr_code": qr_code})
