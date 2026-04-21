import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings 

logger = logging.getLogger('email_notifications')

def send_contact_notification(contact_message):
    """
    Отправка уведомления администратору при получении нового обращения
    """
    try:
        # Формируем данные для письма
        context = {
            'name': contact_message.name,
            'email': contact_message.email,
            'phone': contact_message.phone,
            'message': contact_message.message,
            'created_at': contact_message.created_at.strftime('%d.%m.%Y %H:%M:%S')
        }
        
        # Генерируем текст письма
        subject = _('Новое обращение с формы контактов')
        message = render_to_string('emails/contact_notification.html', context)
        
        # Логируем попытку отправки
        logger.info(
            f"Попытка отправки уведомления для обращения #{contact_message.id}. "
            f"Получатель: {settings.DEFAULT_FROM_EMAIL}, Тема: {subject}"
        )
        
        # Отправляем письмо
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        logger.info(f"Уведомление успешно отправлено для обращения #{contact_message.id}")
        return True
    except Exception as e:
        logger.error(
            f"Ошибка при отправке уведомления для обращения #{contact_message.id}: {str(e)}",
            exc_info=True
        )
        return False