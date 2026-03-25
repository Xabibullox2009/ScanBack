from django.conf import settings


def language_context(request):
    return {
        "current_language": getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE),
        "language_options": settings.LANGUAGES,
    }
