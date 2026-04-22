import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage
from core.util.email import send_contact_notification

logger = logging.getLogger(__name__)

@csrf_protect
@require_http_methods(["GET", "POST"])
def contact_view(request):
    """Страница формы обратной связи с улучшенной защитой от спама"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                # Получаем IP-адрес отправителя
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip_address = x_forwarded_for.split(',')[0]
                else:
                    ip_address = request.META.get('REMOTE_ADDR')
                
                # Сохраняем сообщение
                contact_message = ContactMessage.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    message=form.cleaned_data['message'],
                    ip_address=ip_address
                )
                
                # Отправляем уведомление администратору
                if not send_contact_notification(contact_message):
                    logger.error(
                        _("Не удалось отправить уведомление для обращения #{id}").format(id=contact_message.id)
                    )
                    # Не прерываем выполнение, но добавляем предупреждение
                    messages.warning(request, _('Уведомление не отправлено, но сообщение сохранено.'))
                else:
                    messages.success(request, _('Ваше сообщение успешно отправлено!'))
                
                return redirect('contacts:contact')
                
            except Exception as e:
                logger.error(f"Ошибка при сохранении обращения: {str(e)}")
                messages.error(request, _('Произошла ошибка при отправке сообщения. Попробуйте позже.'))
        else:
            # Логирование ошибок валидации (возможный спам)
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(
                        f"Ошибка валидации формы контактов: поле={field}, ошибка={error}, "
                        f"IP={request.META.get('REMOTE_ADDR', 'unknown')}"
                    )
            messages.error(request, _('Пожалуйста, исправьте ошибки в форме.'))
    else:
        form = ContactForm()
    
    return render(request, 'contacts.html', {'form': form})