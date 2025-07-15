"""
Django REST API views for authentication: login (FusionAuth token reception/exchange),
token validation, and logout, using the FusionAuth JWT utility.

These endpoints are designed for integration with the frontend to provide secure
authentication flows via FusionAuth.

The login endpoint expects a FusionAuth JWT (typically sent from the frontend,
received via redirect or token store). It validates the JWT.

The validate-token endpoint checks the authenticity and validity of a given token.

The logout endpoint performs simple server-side session/token removal, but as JWT
is stateless, logout on the backend typically requires additional handling on the
client/front (such as deleting localStorage/cookies).

All endpoints use the validate_fusionauth_jwt utility for consistency.
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .auth_utils import validate_fusionauth_jwt

from django.core.exceptions import PermissionDenied

# PUBLIC_INTERFACE
@csrf_exempt
def login_view(request):
    """
    POST only. Receives a FusionAuth JWT (id_token or access_token) in JSON body or POST data,
    validates it using the JWT utility, and (optionally) returns claims/user info.

    This endpoint is typically used after the frontend obtains a token via FusionAuth and
    redirects/submits it to the backend.

    Request:
        POST /api/auth/login/
        {
            "token": "<FusionAuth JWT>"
        }

    Response:
        200 OK { "success": true, "claims": { ...jwt_claims... } }
        400/403 if token invalid or missing
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)
    try:
        body = json.loads(request.body.decode())
        token = body.get("token")
    except Exception:
        token = request.POST.get("token")
    if not token:
        return JsonResponse({"error": "Missing token."}, status=400)
    try:
        claims = validate_fusionauth_jwt(token)
        # NOTE: No session is created; frontend manages tokens.
        return JsonResponse({"success": True, "claims": claims})
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=403)

# PUBLIC_INTERFACE
@csrf_exempt
def validate_token_view(request):
    """
    POST only. Validates a FusionAuth JWT provided in the request body, returning decoded claims
    if valid, or an error otherwise.

    Request:
        POST /api/auth/validate-token/
        {
            "token": "<FusionAuth JWT>"
        }

    Response:
        200 OK { "valid": true, "claims": { ... } }
        400/403 if token invalid or missing
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)
    try:
        body = json.loads(request.body.decode())
        token = body.get("token")
    except Exception:
        token = request.POST.get("token")
    if not token:
        return JsonResponse({"error": "Missing token."}, status=400)
    try:
        claims = validate_fusionauth_jwt(token)
        return JsonResponse({"valid": True, "claims": claims})
    except PermissionDenied as e:
        return JsonResponse({"valid": False, "error": str(e)}, status=403)

# PUBLIC_INTERFACE
@csrf_exempt
def logout_view(request):
    """
    POST only. "Logs out" a user. Since JWT authentication is stateless on the backend,
    logging out is a frontend (token deletion) concern. This stub endpoint exists to
    allow the frontend to call for logout events.

    Request:
        POST /api/auth/logout/
        (optionally provide token for future blacklisting implementation)

    Response:
        200 OK { "success": true }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)
    # Could implement JWT blacklist here, if desired.
    return JsonResponse({"success": True})
