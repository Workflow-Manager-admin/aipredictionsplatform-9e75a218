"""
Django settings for Backend_API_Server

This file includes base settings for a Django project and is updated to reference
FusionAuth configuration for JWT authentication, using environment variables.

Note: Other default or required Django settings (DATABASES, etc.) are omitted for brevity and should be included as appropriate for your project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "replace-me-with-a-secret-key-for-dev-only")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Add your API apps here
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Place for custom authentication middleware if needed
]

ROOT_URLCONF = "Backend_API_Server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Backend_API_Server.wsgi.application"

# FusionAuth + JWT Settings (Environment variables)
FUSIONAUTH_ISSUER = os.environ.get("FUSIONAUTH_ISSUER")
FUSIONAUTH_CLIENT_ID = os.environ.get("FUSIONAUTH_CLIENT_ID")
FUSIONAUTH_CLIENT_SECRET = os.environ.get("FUSIONAUTH_CLIENT_SECRET")
FUSIONAUTH_JWT_PUBLIC_KEY = os.environ.get("FUSIONAUTH_JWT_PUBLIC_KEY")

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Example: Configuration to prepare for JWT auth backend integration (additional Django REST Framework settings can be added as needed)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'Backend_API_Server.auth_utils.FusionAuthJWTAuthentication',  # To register custom authentication backend if needed
    ),
}
