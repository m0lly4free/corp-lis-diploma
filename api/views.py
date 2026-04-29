from rest_framework import generics, status, serializers 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
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


@method_decorator(cache_page(1800), name='dispatch')
class ServiceListView(generics.ListAPIView):
    """
    GET /api/services/
    Оптимизация: select_related + prefetch_related + кэш ответа
    """
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('category').prefetch_related('tags').order_by('name')
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"API error in ServiceListView: {str(e)}")
            return Response(
                {'error': _('Ошибка при получении списка услуг')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(cache_page(1800), name='dispatch')
class ServiceDetailView(generics.RetrieveAPIView):
    """
    GET /api/services/<id>/
    """
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('category').prefetch_related('tags')

    def get_object(self):
        try:
            return super().get_object()
        except Service.DoesNotExist:
            raise NotFound(_('Услуга не найдена'))
        except Exception as e:
            logger.error(f"API error in ServiceDetailView: {str(e)}")
            raise NotFound(_('Ошибка при получении услуги'))


@method_decorator(cache_page(900), name='dispatch')
class NewsListView(generics.ListAPIView):
    """
    GET /api/news/
    """
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        return News.objects.filter(is_active=True).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"API error in NewsListView: {str(e)}")
            return Response(
                {'error': _('Ошибка при получении списка новостей')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(cache_page(900), name='dispatch')
class NewsDetailView(generics.RetrieveAPIView):
    """
    GET /api/news/<id>/
    """
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        return News.objects.filter(is_active=True).select_related('author', 'category').prefetch_related('tags')

    def get_object(self):
        try:
            return super().get_object()
        except News.DoesNotExist:
            raise NotFound(_('Новость не найдена'))
        except Exception as e:
            logger.error(f"API error in NewsDetailView: {str(e)}")
            raise NotFound(_('Ошибка при получении новости'))


class ContactMessageCreateView(generics.CreateAPIView):
    """
    POST /api/contact/
    """
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            contact_message = serializer.save(ip_address=ip_address)
            
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
            logger.warning(
                f"Попытка спама: {e.detail}, IP={request.META.get('REMOTE_ADDR', 'unknown')}"
            )
            return Response(
                {'error': _('Ошибка валидации'), 'details': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"API error in ContactMessageCreateView: {str(e)}")
            return Response(
                {'error': _('Ошибка при отправке сообщения')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(cache_page(1800), name='dispatch')
class PageDetailView(generics.RetrieveAPIView):
    """
    GET /api/page/<slug>/
    """
    serializer_class = PageSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)

    def get_object(self):
        try:
            return super().get_object()
        except Page.DoesNotExist:
            raise NotFound(_('Страница не найдена'))
        except Exception as e:
            logger.error(f"API error in PageDetailView: {str(e)}")
            raise NotFound(_('Ошибка при получении страницы'))