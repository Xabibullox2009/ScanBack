import os
import uuid

import qrcode
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import QRCode


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if not name or not phone:
            return render(request, "qrhub/home.html", {"error": "Barcha maydonlarni to'ldiring!"})

        qr = QRCode(name=name, phone=phone)
        qr.save()

        base_url = getattr(settings, "SCANBACK_BASE_URL", request.build_absolute_uri("/")[:-1])
        url = f"{base_url}/u/{qr.slug}/"

        qr_path = os.path.join(settings.MEDIA_ROOT, "qr_codes")
        os.makedirs(qr_path, exist_ok=True)

        qr_image_path = os.path.join(qr_path, f"{qr.slug}.png")

        img = qrcode.make(url)
        img.save(qr_image_path)

        qr.qr_image = f"qr_codes/{qr.slug}.png"
        qr.save()

        return redirect("qrhub:result", slug=qr.slug)

    return render(request, "qrhub/home.html")


def result(request, slug):
    try:
        qr = QRCode.objects.get(slug=slug)
    except QRCode.DoesNotExist:
        return render(request, "qrhub/not_found.html", status=404)

    return render(request, "qrhub/result.html", {"qr": qr})


def detail(request, slug):
    try:
        qr = QRCode.objects.get(slug=slug)
    except QRCode.DoesNotExist:
        return render(request, "qrhub/not_found.html", status=404)

    phone_link = qr.phone.replace(" ", "").replace("-", "")

    return render(request, "qrhub/detail.html", {"qr": qr, "phone_link": phone_link})
