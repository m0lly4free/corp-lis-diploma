import os
try:
    from decouple import config
except ImportError:
    import os
    config = lambda key, default=None: os.environ.get(key, default)

from datetime import timedelta
from pathlib import Path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps', 
    'django.contrib.sites',     
    'rest_framework',
    'corsheaders',
    'axes',
    'core',
    'services',
    'news',
    'contacts',
    'pages',
    'users',
    'api',
]
SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'corp_lis.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['/app/templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'core.context_processors.analytics_context',
        ],
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'corp_lis',
        'USER': 'corp_lis_user',
        'PASSWORD': 'corp_lis_pass',
        'HOST': 'db',
        'PORT': '5432',
        
    }
}
# Статические файлы
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# Настройки статики
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SECRET_KEY = config('SECRET_KEY', default='fallback-key-123')

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Безопасность - БАЗОВЫЕ НАСТРОЙКИ
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF защита (включена по умолчанию в Django)
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

# Сессии
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 час
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Аутентификация
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/'

DEBUG = config('DEBUG', default=True, cast=bool)
# Django Axes - ограничение попыток входа
if not DEBUG:
    AXES_ENABLED = True
if DEBUG:
    AXES_ENABLED = False

AXES_FAILURE_LIMIT = 5  
AXES_COOLOFF_TIME = timedelta(minutes=30)  
AXES_LOCKOUT_CALLABLE = 'axes.helpers.lockout_response'
AXES_RESET_ON_SUCCESS = True  # Сброс счетчика при успешном входе
AXES_META_PRECEDENCE_ORDER = [
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR',
]
# В настройках django-axes добавьте:
AXES_USE_USER_AGENT = False  # ← ВАЖНО: Отключаем User-Agent
AXES_SESSION_KEY = 'axes_session_hash'  # ← Фиксируем ключ сессии
AXES_USE_SESSION = True  # ← Убедитесь, что сессия используется

# CORS (если используется API)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",

]

# Разрешенные форматы файлов
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'svg']
ALLOWED_DOCUMENT_EXTENSIONS = ['pdf']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Для генерации миниатюр
THUMBNAIL_SIZE = (300, 300)

import os

# Директория для логов
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'spam_formatter': {
            'format': '{levelname} {asctime} {module} IP:{ip} {message}',
            'style': '{',
        },
        'api_formatter': {
            'format': '{levelname} {asctime} {module} API {message}',
            'style': '{',
        },
        'error_formatter': {
            'format': '{levelname} {asctime} {module} {pathname}:{lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'admin_actions.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'email_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'email_notifications.log'),
            'formatter': 'verbose',
        },
        'spam_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'spam_attempts.log'),
            'formatter': 'spam_formatter',
        },
        'api_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'api_errors.log'),
            'formatter': 'api_formatter',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'system_errors.log'),
            'formatter': 'error_formatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'axes.watch_login': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'email_notifications': {
            'handlers': ['email_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'spam_protection': {
            'handlers': ['spam_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'api_errors': {
            'handlers': ['api_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'system_errors': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Кэширование для ускорения работы админ-панели
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
DEBUG = config('DEBUG', default=True, cast=bool)
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'corp-lis-cache',
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }

# Настройки кеширования страниц
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300  # 5 минут
CACHE_MIDDLEWARE_KEY_PREFIX = 'corp_lis'

# Заголовки Cache-Control
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True if not DEBUG else False
SECURE_HSTS_PRELOAD = True if not DEBUG else False
# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Аналитика
YANDEX_METRIKA_ID = config('YANDEX_METRIKA_ID', default='')
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')

# Флаг для включения аналитики (по умолчанию выключена)
ENABLE_ANALYTICS = config('ENABLE_ANALYTICS', default=False, cast=bool)

# Настройки электронной почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@corp-lis.ru')

#сайтмап
SITEMAP_URL = 'http://localhost:8000/sitemap.xml'

# Создание директории для логов
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# DEBUG режим (по умолчанию True для разработки)
DEBUG = config('DEBUG', default=True, cast=bool)

# Соответствие ТЗ 3.2.8 - Использование HTTPS
# В production (DEBUG=False) автоматически включаются все HTTPS-настройки
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    handler404 = 'django.views.defaults.page_not_found'
    handler500 = 'django.views.defaults.server_error'
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    handler404 = 'core.views.custom_404'
    handler500 = 'core.views.custom_500'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    MIDDLEWARE.insert(1, 'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')
else:
    # В режиме разработки отключаем HTTPS для локального тестирования
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

# Настройки Cache-Control для статических файлов
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

DEBUG=False