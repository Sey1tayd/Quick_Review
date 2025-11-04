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
    Modifies the request META before SecurityMiddleware validates it.
    Must run BEFORE SecurityMiddleware in MIDDLEWARE settings.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we're on Railway and if the host is a Railway domain
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
            host = request.get_host().split(':')[0]  # Remove port if present
            # Allow any Railway domain (*.railway.app)
            if host.endswith('.railway.app') or host == 'railway.app':
                # Store original host for reference
                if not hasattr(request, '_original_host'):
                    request._original_host = request.META.get('HTTP_HOST')
                # Modify HTTP_HOST to 'localhost' temporarily to pass ALLOWED_HOSTS check
                # SecurityMiddleware will validate against ALLOWED_HOSTS, so we use a known good host
                request.META['HTTP_HOST'] = 'localhost'
                # Also set SERVER_NAME to avoid issues
                request.META['SERVER_NAME'] = 'localhost'
        
        return self.get_response(request)

