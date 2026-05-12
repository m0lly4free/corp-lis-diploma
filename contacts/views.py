import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings

from .forms import ContactForm
from .models import ContactMessage
from core.util.email import send_contact_notification
from .serializers import ContactMessageSerializer

from rest_framework.permissions import AllowAny
from rest_framework import generics

logger = logging.getLogger(__name__)


# ==========================================
# API View (для отправки через AJAX/Fetch)
# ==========================================
class ContactMessageCreateView(generics.CreateAPIView):
    """
    API точка для создания обращения.
    Валидация происходит автоматически через Serializer (ТЗ 5.5).
    """
    model = ContactMessage  # ← Исправлено на model
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


# ==========================================
# Functional View (для классической HTML формы)
# ==========================================
@cache_page(60 * 5)  # Кэш страницы на 5 минут
@csrf_protect        # Защита от CSRF
@require_http_methods(["GET", "POST"])
def contact_view(request):
    """Страница формы обратной связи"""
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                # 1. Получаем IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
                
                # 2. Проверка на спам (Лимит: 3 запроса за 5 минут)
                spam_cache_key = f"contact_spam_{ip_address}"
                spam_count = cache.get(spam_cache_key, 0)
                
                if spam_count >= 3:
                    logger.warning(f"Spam detected from IP {ip_address}")
                    messages.error(request, _('Слишком много попыток. Попробуйте позже.'))
                    return render(request, 'contacts.html', {'form': form})
                
                # 3. Сохраняем в БД
                contact_message = form.save() 
                contact_message.ip_address = ip_address
                contact_message.save()
                
                # 4. Увеличиваем счетчик спама
                cache.set(spam_cache_key, spam_count + 1, 300) 
                
                # 5. Отправка уведомления
                try:
                    send_contact_notification(contact_message)
                    messages.success(request, _('Ваше сообщение успешно отправлено!'))
                except Exception as email_err:
                    logger.error(f"Email notification failed: {email_err}")
                    messages.warning(request, _('Сообщение сохранено, но уведомление не отправлено.'))
                
                # 6. Редирект (чтобы не отправлять повторно при F5)
                return redirect('contacts:contact')
                
            except Exception as e:
                logger.error(f"Critical error saving message: {str(e)}")
                messages.error(request, _('Произошла ошибка при сохранении.'))
        else:
            # Форма не валидна (ошибки валидации)
            logger.warning(f"Validation failed for IP {request.META.get('REMOTE_ADDR')}")
            messages.error(request, _('Пожалуйста, исправьте ошибки в форме.'))
            
    else:
        form = ContactForm()

    return render(request, 'contacts.html', {'form': form})