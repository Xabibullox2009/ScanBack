from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import QRCode


def public_page(request, slug):
    qr = get_object_or_404(QRCode, slug=slug)
    phone_link = qr.get_tel_link()
    return render(request, "qrhub/public.html", {"qr": qr, "phone_link": phone_link})

def index(request):
    return HttpResponse("Home page")