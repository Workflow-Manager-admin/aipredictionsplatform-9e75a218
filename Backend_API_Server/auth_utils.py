"""
Utility module for FusionAuth JWT validation and user authentication.

This module provides a function for validating and decoding JWTs issued by FusionAuth,
using environment variables for configuration and python-jose for signature/certificate verification.

To use, import and call 'validate_fusionauth_jwt(token)' in your views/middleware.
"""

import os
from jose import jwt, JWTError, ExpiredSignatureError
from jose.constants import ALGORITHMS

from django.conf import settings
from django.core.exceptions import PermissionDenied
from typing import Dict, Any

# PUBLIC_INTERFACE
def validate_fusionauth_jwt(token: str) -> Dict[str, Any]:
    """
    Validates and decodes a JWT issued by FusionAuth.

    Args:
        token (str): JWT token string.

    Returns:
        dict: Decoded claims on success.

    Raises:
        PermissionDenied: If the token is invalid, expired, or fails verification.
    """
    issuer = os.environ.get("FUSIONAUTH_ISSUER")
    client_id = os.environ.get("FUSIONAUTH_CLIENT_ID")
    public_key = os.environ.get("FUSIONAUTH_JWT_PUBLIC_KEY")

    if not issuer or not client_id or not public_key:
        raise PermissionDenied("FusionAuth configuration missing.")

    try:
        # The public key should be in PEM format
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[ALGORITHMS.RS256],
            audience=client_id,
            issuer=issuer,
            options={
                "verify_signature": True,
                "verify_aud": True,
                "verify_iat": True,
                "verify_exp": True,
                "verify_iss": True,
            }
        )
        return payload
    except ExpiredSignatureError:
        raise PermissionDenied("Token has expired.")
    except JWTError as e:
        raise PermissionDenied(f"Invalid token: {str(e)}")


# Example stub for a possible DRF/Django authentication backend (for future endpoint integration)
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class FusionAuthJWTAuthentication(BaseAuthentication):
    """
    Custom DRF authentication backend to authenticate requests using FusionAuth JWT.
    """

    # PUBLIC_INTERFACE
    def authenticate(self, request):
        """Authenticate the request and return a user object and auth data."""
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1]
        try:
            payload = validate_fusionauth_jwt(token)
        except PermissionDenied as e:
            raise exceptions.AuthenticationFailed(str(e))

        # For a production system, you would now retrieve (or create) a Django user based on the JWT claims.
        # Here we just return None for user so view can check payload manually, or extend as needed.
        return (None, payload)
