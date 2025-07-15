"""
FusionAuth JWT Middleware and Token Management for Django APIs.

- Provides middleware to extract and validate JWTs on protected API endpoints.
- Uses 'Authorization: Bearer <token>' standard header.
- Employs the validate_fusionauth_jwt utility.
- Prepare stubs for refresh/blacklist infrastructure.

To protect a Django view or endpoint, add this middleware class to your MIDDLEWARE or use the decorator below.

Note: Blacklist/refresh functionality is documented but not implemented (requires data store and session management).
"""

import re
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .auth_utils import validate_fusionauth_jwt

def _extract_bearer_token(request):
    """Extracts 'Bearer <token>' from Authorization header."""
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    match = re.match(r"^Bearer (.+)$", auth)
    return match.group(1) if match else None

# PUBLIC_INTERFACE
class FusionAuthJWTMiddleware(MiddlewareMixin):
    """
    Middleware to enforce FusionAuth JWT validation on routes under /api/protected/.
    Rejects requests with missing or invalid tokens.

    Add 'Backend_API_Server.jwt_middleware.FusionAuthJWTMiddleware' to MIDDLEWARE in settings.py
    (or use as a per-view decorator for granular control).

    Optionally, adapt 'process_view' to target more/less endpoints as needed.
    """

    # PUBLIC_INTERFACE
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Only enforce JWT auth on routes starting with /api/protected/
        if not request.path.startswith("/api/protected/"):
            return None  # Allow unprotected routes

        token = _extract_bearer_token(request)
        if not token:
            return JsonResponse({"error": "Missing or malformed Authorization token."}, status=401)

        try:
            claims = validate_fusionauth_jwt(token)
            request.jwt_claims = claims
        except PermissionDenied as exc:
            return JsonResponse({"error": str(exc)}, status=403)
        # If successful, allow the request to proceed.

        # --- (Optional for future) Blacklist support ---
        # If using a token blacklist, check here if token is blacklisted.
        # If found in blacklist: return JsonResponse({"error": "Token blacklisted."}, status=401)

        # --- (Optional for future) Refresh support ---
        # If implementing refresh tokens, check token type here and deny use of refresh token for protected endpoints.

        return None

# PUBLIC_INTERFACE
def jwt_required(view_func):
    """
    Decorator version of the JWT check for class/function-based views.

    Usage: 
        @jwt_required
        def my_view(request): ...
    """
    from functools import wraps

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = _extract_bearer_token(request)
        if not token:
            return JsonResponse({"error": "Missing or malformed Authorization token."}, status=401)
        try:
            claims = validate_fusionauth_jwt(token)
            request.jwt_claims = claims
        except PermissionDenied as exc:
            return JsonResponse({"error": str(exc)}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# --- Blacklist utilities (future implementation example) ---
def is_token_blacklisted(token):
    """
    Stub for token blacklist lookup (implement persistent store/DB/redis as needed).
    """
    # Example: return redis_client.exists(f"blacklist:{token}")
    return False

def blacklist_token(token):
    """
    Stub for blacklisting tokens (implement persistent store/DB/redis as needed).
    """
    # Example: redis_client.setex(f"blacklist:{token}", expiry_seconds, 1)
    pass

