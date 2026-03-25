from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation

from .models import QRCode


def home(request):
    return render(request, "qrhub/home.html")


def public_qr(request, slug):
    qr_code = get_object_or_404(QRCode, slug=slug)
    return render(request, "qrhub/public.html", {"qr_code": qr_code})


def switch_language(request):
    language_code = request.GET.get("lang", settings.LANGUAGE_CODE)
    supported_languages = {code for code, _ in settings.LANGUAGES}
    if language_code not in supported_languages:
        language_code = settings.LANGUAGE_CODE

    request.session["language_code"] = language_code
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    response = redirect(next_url)
    translation.activate(language_code)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    return response
