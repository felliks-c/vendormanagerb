import os
from django.conf import settings
from django.http import JsonResponse

# app/middleware/verify_secret.py
# Django middleware: проверяет заголовок API_SHARED_SECRET в каждом запросе



class VerifySecretMiddleware:
    """
    Проверяет наличие и значение заголовка API_SHARED_SECRET.
    Ожидаемое значение берется из settings.API_SHARED_SECRET или переменной окружения API_SHARED_SECRET.
    Если секрет не настроен — возвращается 500. Если заголовок отсутствует или неверен — 401.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # приоритет: settings -> env
        self.expected = getattr(settings, "API_SHARED_SECRET", None) or os.environ.get("API_SHARED_SECRET")

    def __call__(self, request):
        # Django автоматически помещает заголовки в request.META с префиксом HTTP_
        header_value = request.META.get("HTTP_API_SHARED_SECRET")

        if not self.expected:
            return JsonResponse({"detail": "Server API_SHARED_SECRET is not configured"}, status=500)

        if not header_value or header_value != self.expected:
            return JsonResponse({"detail": "API_SHARED_SECRET missing or invalid"}, status=401)

        return self.get_response(request)