from django.conf import settings
from django.utils.translation import get_language


def language_context(request):
    return {
        "current_language": get_language() or settings.LANGUAGE_CODE,
        "language_options": settings.LANGUAGES,
    }
