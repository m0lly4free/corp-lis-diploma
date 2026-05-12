from django.conf import settings

def analytics_context(request):
    """
    Контекстный процессор для передачи настроек аналитики в шаблоны
    """
    return {
        'YANDEX_METRIKA_ID': getattr(settings, 'YANDEX_METRIKA_ID', ''),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        'ENABLE_ANALYTICS': getattr(settings, 'ENABLE_ANALYTICS', False),
    }