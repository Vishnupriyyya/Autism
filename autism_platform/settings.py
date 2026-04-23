"""
Django settings for Autism Learning and Skill Development Platform.
Supports GCP (Cloud Storage, Cloud SQL) for scalability.
Production-ready for Cloud Run: WhiteNoise for statics, env vars required.
"""
import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security - REQUIRED ENV VARS for Cloud Run: DJANGO_SECRET_KEY, DEBUG=false, ALLOWED_HOSTS=*.run.app
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-in-production-use-env-var-DO-NOT-USE"
)
# Generated secure key (use this in Cloud Run Secrets): django-insecure-autism-platform-cloud-run-2024#kX9pL2mQ8vR5tY7uW3sE6nJ1hZ4bC0fG!
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'https://autism-310236859100.asia-south1.run.app'
]
# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "children",
    "learning",
    "recommendations",
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "autism_platform.urls"
WSGI_APPLICATION = "autism_platform.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database - supports SQLite (dev) and Cloud SQL (prod via GCP)
# For Cloud Run: SQLite is ephemeral (data lost on restart)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# GCP Cloud SQL (uncomment and configure for production)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("GCP_DB_NAME", "autism_platform"),
#         "USER": os.environ.get("GCP_DB_USER", ""),
#         "PASSWORD": os.environ.get("GCP_DB_PASSWORD", ""),
#         "HOST": os.environ.get("GCP_DB_HOST", "/cloudsql/my-autism-project-id:us-central1:autism-db"),
#         "PORT": os.environ.get("GCP_DB_PORT", "5432"),
#     }
# }

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (WhiteNoise handles serving)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files - local or GCP Cloud Storage (ephemeral on Cloud Run)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# GCP Cloud Storage for media (images, audio, video) - recommended for persistence
# pip install django-storages google-cloud-storage
# DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# GS_BUCKET_NAME = os.environ.get("GCP_STORAGE_BUCKET", "autism-platform-media")
# GS_DEFAULT_ACL = "publicRead"

# Login/Logout URLs
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:role_redirect"
LOGOUT_REDIRECT_URL = "home"

# Session
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 86400  # 24 hours

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cloud Run prod notes
# Set SECURE_SSL_REDIRECT = True in prod (HTTPS enforced)
# CSRF_TRUSTED_ORIGINS = ['https://your-service-xxx.a.run.app']
