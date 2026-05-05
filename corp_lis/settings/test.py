"""
Тестовые настройки для АО «Корпорация ЛИС»
"""
from .base import *

DEBUG = False
TESTING = True

# ===== БАЗА ДАННЫХ =====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# ===== КЭШИРОВАНИЕ =====
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# ===== СЕССИИ =====
# ✅ ИСПОЛЬЗУЕМ БД ДЛЯ СЕССИЙ, так как DummyCache не работает с cache-сессиями
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ===== ПАРОЛИ =====
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = []

# ===== СТАТИКА =====
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
if 'ManifestStaticFilesStorage' in str(globals().get('STATICFILES_STORAGE', '')):
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# ===== EMAIL =====
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# ===== ЛОГИРОВАНИЕ =====
LOGGING['loggers']['django']['level'] = 'WARNING'