from django.conf import settings
from django.utils import translation


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = {code for code, _ in settings.LANGUAGES}

    def __call__(self, request):
        language_code = request.session.get("language_code", settings.LANGUAGE_CODE)
        if language_code not in self.supported_languages:
            language_code = settings.LANGUAGE_CODE

        request.LANGUAGE_CODE = language_code
        translation.activate(language_code)
        response = self.get_response(request)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
        translation.deactivate()
        return response
