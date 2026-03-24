from django.shortcuts import get_object_or_404, redirect, render

from .models import QRCode


def home(request):
    return redirect("admin:index")


def public_qr(request, slug):
    qr_code = get_object_or_404(QRCode, slug=slug)
    return render(request, "qrhub/public.html", {"qr_code": qr_code})
