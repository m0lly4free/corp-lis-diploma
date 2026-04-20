import os
try:
    from decouple import config
except ImportError:
    import os
    config = lambda key, default=None: os.environ.get(key, default)

from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'axes',  # ← ДОЛЖНО БЫТЬ ЗДЕСЬ
    'core',
    'services',
    'news',
    'contacts',
    'pages',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'axes.middleware.AxesMiddleware',  # ← ДОЛЖНО БЫТЬ ЗДЕСЬ
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
    'axes.backends.AxesStandaloneBackend',  # ← ДОЛЖНО БЫТЬ ЗДЕСЬ
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

# Django Axes - ограничение попыток входа
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5  # Максимум 5 неудачных попыток
AXES_COOLOFF_TIME = timedelta(minutes=30)  # Блокировка на 30 минут
AXES_LOCKOUT_CALLABLE = 'axes.helpers.lockout_response'
AXES_RESET_ON_SUCCESS = True  # Сброс счетчика при успешном входе
AXES_META_PRECEDENCE_ORDER = [
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR',
]

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
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'admin_actions.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'axes.watch_login': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Создание директории для логов
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# DEBUG режим (по умолчанию True для разработки)
DEBUG = config('DEBUG', default=True, cast=bool)

# ВАЖНО: НЕ ДОБАВЛЯЙТЕ НИКАКИХ HTTPS-НАСТРОЕК В РЕЖИМЕ РАЗРАБОТКИ
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
else:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True