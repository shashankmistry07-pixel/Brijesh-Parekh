"""
Django settings for silverstar project (Brijesh Parekh Official Website).
Optimized for high performance, caching, and production/live deployment.
"""

from pathlib import Path
import os
import mimetypes

# MIME types configuration
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)
mimetypes.add_type("video/mp4", ".mp4", True)
mimetypes.add_type("video/quicktime", ".mov", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings (Environment variables with safe defaults for development)
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-9set8)ic9paczcz4g4k$+w_#6grwdi5h&hpr@o&o-u_!w324*-'
)

# DEBUG setting
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes', 't')

# Host and Domain Configurations
ALLOWED_HOSTS = ['*']

# CSRF Trusted Origins for Live Deployment (Vercel, Render, Railway, Custom Domains)
CSRF_TRUSTED_ORIGINS = [
    'https://brijesh-parekh.vercel.app',
    'https://*.vercel.app',
    'https://*.onrender.com',
    'https://*.railway.app',
    'http://localhost',
    'http://127.0.0.1',
]
custom_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if custom_origins:
    CSRF_TRUSTED_ORIGINS.extend([o.strip() for o in custom_origins.split(',') if o.strip()])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'singer_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for fast static asset delivery
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'silverstar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'singer_app.context_processors.profile_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'silverstar.wsgi.application'
ASGI_APPLICATION = 'silverstar.asgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 60,  # Persistent connections for faster queries
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images, Media)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'
os.makedirs(STATIC_ROOT, exist_ok=True)


# Modern Django 4.2+ and 5.x Storage Configuration with WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Static file caching duration (1 year in seconds for production)
WHITENOISE_MAX_AGE = 31536000

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration (Gmail SMTP Integration)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'brijesh71090parekh@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'oydcymayoffnqryf')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Brijesh Parekh Official <brijesh71090parekh@gmail.com>')
ADMIN_NOTIFICATION_EMAIL = os.environ.get('ADMIN_NOTIFICATION_EMAIL', 'brijesh71090parekh@gmail.com')

# Production Security Enhancements
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
