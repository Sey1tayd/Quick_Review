"""
Custom middleware to handle healthcheck endpoint for Railway
"""
from django.http import HttpResponse


class HealthcheckMiddleware:
    """
    Middleware that handles healthcheck endpoint specially.
    Returns OK immediately for healthcheck requests, bypassing ALLOWED_HOSTS check.
    This must be placed before SecurityMiddleware in MIDDLEWARE settings.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # For healthcheck endpoint, return OK immediately before any other middleware
        if request.path == '/health/':
            return HttpResponse("OK", status=200)
        
        return self.get_response(request)

