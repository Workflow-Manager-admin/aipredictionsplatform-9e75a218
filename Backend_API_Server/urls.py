"""
URL configuration for Backend_API_Server authentication and API endpoints.

Defines routes for authentication endpoints:
- /api/auth/login/      [POST] - Accept and validate FusionAuth token
- /api/auth/validate-token/ [POST] - Validate token and return claims
- /api/auth/logout/     [POST] - Stub endpoint for frontend-initiated logout

Add additional API endpoints to this file as needed.
"""

from django.urls import path

from .views import login_view, validate_token_view, logout_view

urlpatterns = [
    path("api/auth/login/", login_view, name="login"),
    path("api/auth/validate-token/", validate_token_view, name="validate_token"),
    path("api/auth/logout/", logout_view, name="logout"),
]
