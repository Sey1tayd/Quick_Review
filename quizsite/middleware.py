"""
Custom middleware to handle healthcheck endpoint and Railway domains
"""
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
import os


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


class RailwayAllowedHostsMiddleware:
    """
    Middleware that allows Railway domains to bypass ALLOWED_HOSTS check.
    This handles Railway's dynamic domains (*.railway.app).
    Dynamically adds Railway domains to ALLOWED_HOSTS.
    Must run BEFORE SecurityMiddleware in MIDDLEWARE settings.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Import settings here to avoid circular import
        from django.conf import settings
        
    def __call__(self, request):
        # Check if we're on Railway
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
            # Get host directly from META to avoid SuspiciousOperation
            host = request.META.get('HTTP_HOST', '').split(':')[0]  # Remove port if present
            # Allow any Railway domain (*.railway.app)
            if host and (host.endswith('.railway.app') or host == 'railway.app'):
                # Dynamically add to ALLOWED_HOSTS if not already there
                from django.conf import settings
                if host not in settings.ALLOWED_HOSTS:
                    settings.ALLOWED_HOSTS.append(host)
        
        return self.get_response(request)

