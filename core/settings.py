import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key – read from environment variable (set on Render)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-me')

# Turn off debug
DEBUG = False

# Allow any host during deployment (Render will provide its own domain)
ALLOWED_HOSTS = ['*']

# Add Whitenoise middleware (for static files)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # <-- add this line
    # ... keep your other middleware
]

# Database – use DATABASE_URL environment variable (provided by Render)
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/edupredict',
        conn_max_age=600
    )
}

# Static files (CSS, JS, images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads) – for demo, local storage is fine
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'