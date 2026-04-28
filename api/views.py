from rest_framework import generics, status, serializers 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from services.models import Service
from news.models import News
from contacts.models import ContactMessage
from pages.models import Page
from .serializers import (
    ServiceSerializer, 
    NewsSerializer, 
    ContactMessageSerializer, 
    PageSerializer
)
from core.util.email import send_contact_notification
import logging 
logger = logging.getLogger('api_errors')

class ServiceListView(generics.ListAPIView):
    """
    Получение списка услуг с кэшированием и оптимизацией
    GET /api/services/
    Время ответа: < 300 мс
    Поддержка до 50 одновременных пользователей
    """
    queryset = Service.objects.filter(is_active=True).order_by('name')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        # Кэширование списка услуг на 30 минут
        cache_key = 'api_services_list'
        services = cache.get(cache_key)
        if services is None:
            services = list(Service.objects.filter(is_active=True).order_by('name'))
            cache.set(cache_key, services, 1800)  # 30 минут
        return services
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"API error in ServiceListView: {str(e)}")
            return Response(
                {'error': _('Ошибка при получении списка услуг')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ServiceDetailView(generics.RetrieveAPIView):
    """
    Получение конкретной услуги с кэшированием и оптимизацией
    GET /api/services/<id>/
    Время ответа: < 300 мс
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_object(self):
        service_id = self.kwargs.get('id')
        cache_key = f'api_service_{service_id}'
        obj = cache.get(cache_key)
        
        if obj is None:
            try:
                obj = super().get_object()
                cache.set(cache_key, obj, 1800)  # 30 минут
            except Service.DoesNotExist:
                raise NotFound(_('Услуга не найдена'))
            except Exception as e:
                logger.error(f"API error in ServiceDetailView: {str(e)}")
                raise NotFound(_('Ошибка при получении услуги'))
        
        return obj

class NewsListView(generics.ListAPIView):
    """
    Получение списка новостей с кэшированием и оптимизацией
    GET /api/news/
    Время ответа: < 300 мс
    Поддержка до 50 одновременных пользователей
    """
    queryset = News.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        # Кэширование списка новостей на 15 минут
        cache_key = 'api_news_list'
        news_list = cache.get(cache_key)
        if news_list is None:
            news_list = list(News.objects.filter(is_active=True).order_by('-created_at'))
            cache.set(cache_key, news_list, 900)  # 15 минут
        return news_list
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"API error in NewsListView: {str(e)}")
            return Response(
                {'error': _('Ошибка при получении списка новостей')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NewsDetailView(generics.RetrieveAPIView):
    """
    Получение конкретной новости с кэшированием и оптимизацией
    GET /api/news/<id>/
    Время ответа: < 300 мс
    """
    queryset = News.objects.filter(is_active=True)
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_object(self):
        news_id = self.kwargs.get('id')
        cache_key = f'api_news_{news_id}'
        obj = cache.get(cache_key)
        
        if obj is None:
            try:
                obj = super().get_object()
                cache.set(cache_key, obj, 900)  # 15 минут
            except News.DoesNotExist:
                raise NotFound(_('Новость не найдена'))
            except Exception as e:
                logger.error(f"API error in NewsDetailView: {str(e)}")
                raise NotFound(_('Ошибка при получении новости'))
        
        return obj

class ContactMessageCreateView(generics.CreateAPIView):
    """
    Отправка данных формы обратной связи с защитой от спама и оптимизацией
    POST /api/contact/
    Время ответа: < 300 мс
    Поддержка до 50 одновременных пользователей
    """
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Получаем IP-адрес отправителя
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Сохраняем сообщение с IP-адресом
            contact_message = serializer.save(ip_address=ip_address)
            
            # Отправляем уведомление администратору
            if not send_contact_notification(contact_message):
                logger.error(
                    _("Не удалось отправить уведомление для обращения #{id}").format(id=contact_message.id)
                )
            
            headers = self.get_success_headers(serializer.data)
            return Response(
                {'message': _('Ваше сообщение успешно отправлено!')}, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except serializers.ValidationError as e:
            # Логирование попыток спама
            logger.warning(
                f"Попытка отправки спама через API: {e.detail}, "
                f"IP={request.META.get('REMOTE_ADDR', 'unknown')}"
            )
            return Response(
                {'error': _('Ошибка валидации данных'), 'details': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"API error in ContactMessageCreateView: {str(e)}")
            return Response(
                {'error': _('Ошибка при отправке сообщения')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PageDetailView(generics.RetrieveAPIView):
    """
    Получение статической страницы по slug с кэшированием и оптимизацией
    GET /api/page/<slug>/
    Время ответа: < 300 мс
    """
    queryset = Page.objects.filter(is_active=True)
    serializer_class = PageSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_object(self):
        page_slug = self.kwargs.get('slug')
        cache_key = f'api_page_{page_slug}'
        obj = cache.get(cache_key)
        
        if obj is None:
            try:
                obj = super().get_object()
                cache.set(cache_key, obj, 1800)  # 30 минут
            except Page.DoesNotExist:
                raise NotFound(_('Страница не найдена'))
            except Exception as e:
                logger.error(f"API error in PageDetailView: {str(e)}")
                raise NotFound(_('Ошибка при получении страницы'))
        
        return obj