DEBUG = False

SECURE_SSL_REDIRECT = True  # Принудительный HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 год (365 дней * 24 часа * 60 минут * 60 секунд)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True  # Cookie только по HTTPS
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True  # Защита от MIME-sniffing
X_FRAME_OPTIONS = 'DENY'  # Запрет отображения в iframe
SECURE_BROWSER_XSS_FILTER = True  # Встроенный XSS-фильтр браузера
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'