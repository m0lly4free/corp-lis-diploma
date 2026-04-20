import logging
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

logger = logging.getLogger('django')

class SecureAdminMixin:
    """Миксин для безопасной админ-панели с расширенным логированием"""
    
    def log_addition(self, request, object, message):
        super().log_addition(request, object, message)
        logger.info(f'Пользователь {request.user.username} создал объект: {object}')
    
    def log_change(self, request, object, message):
        super().log_change(request, object, message)
        logger.info(f'Пользователь {request.user.username} изменил объект: {object}')
    
    def log_deletion(self, request, object, object_repr):
        super().log_deletion(request, object, object_repr)
        logger.info(f'Пользователь {request.user.username} удалил объект: {object_repr}')