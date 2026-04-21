from rest_framework import generics, status, serializers 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
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
logger = logging.getLogger(__name__)

class ServiceListView(generics.ListAPIView):
    """
    Получение списка услуг
    GET /api/services/
    """
    queryset = Service.objects.filter(is_active=True).order_by('name')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': _('Ошибка при получении списка услуг')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ServiceDetailView(generics.RetrieveAPIView):
    """
    Получение конкретной услуги
    GET /api/services/<id>/
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_object(self):
        try:
            return super().get_object()
        except Service.DoesNotExist:
            raise NotFound(_('Услуга не найдена'))
        except Exception as e:
            raise NotFound(_('Ошибка при получении услуги'))

class NewsListView(generics.ListAPIView):
    """
    Получение списка новостей
    GET /api/news/
    """
    queryset = News.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': _('Ошибка при получении списка новостей')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NewsDetailView(generics.RetrieveAPIView):
    """
    Получение конкретной новости
    GET /api/news/<id>/
    """
    queryset = News.objects.filter(is_active=True)
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_object(self):
        try:
            return super().get_object()
        except News.DoesNotExist:
            raise NotFound(_('Новость не найдена'))
        except Exception as e:
            raise NotFound(_('Ошибка при получении новости'))

class ContactMessageCreateView(generics.CreateAPIView):
    """
    Отправка данных формы обратной связи
    POST /api/contact/
    """
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {'message': _('Ваше сообщение успешно отправлено!')}, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except serializers.ValidationError as e:
            return Response(
                {'error': _('Ошибка валидации данных'), 'details': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': _('Ошибка при отправке сообщения')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PageDetailView(generics.RetrieveAPIView):
    """
    Получение статической страницы по slug
    GET /api/page/<slug>/
    """
    queryset = Page.objects.filter(is_active=True)
    serializer_class = PageSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_object(self):
        try:
            return super().get_object()
        except Page.DoesNotExist:
            raise NotFound(_('Страница не найдена'))
        except Exception as e:
            raise NotFound(_('Ошибка при получении страницы'))
        
class ContactMessageCreateView(generics.CreateAPIView):
    """
    Отправка данных формы обратной связи
    POST /api/contact/
    """
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            contact_message = serializer.instance  # Получаем сохраненный объект
            
            # Используем исправленный импорт
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
            return Response(
                {'error': _('Ошибка валидации данных'), 'details': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': _('Ошибка при отправке сообщения')}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )