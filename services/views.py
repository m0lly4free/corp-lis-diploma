from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Service
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# Функциональное представление для списка услуг (для совместимости)
@cache_page(60 * 30)  # Кэширование на 30 минут
def services_list(request):
    """Страница списка всех услуг с оптимизацией производительности"""
    try:
        services = Service.objects.filter(is_active=True).select_related().order_by('name')
        context = {
            'services': services,
        }
        return render(request, 'services/index.html', context)
    except Exception as e:
        logger.error(f"Error in services_list: {str(e)}")
        raise

# Функциональное представление для детальной страницы услуги (для совместимости)
@cache_page(60 * 30)  # Кэширование на 30 минут
def service_detail(request, slug):
    """Страница конкретной услуги с оптимизацией производительности"""
    try:
        service = get_object_or_404(Service, slug=slug, is_active=True)
        context = {
            'service': service,
        }
        return render(request, 'services/detail.html', context)
    except Http404:
        logger.warning(f"Service not found: {slug}")
        raise
    except Exception as e:
        logger.error(f"Error in service_detail: {str(e)}")
        raise

# Классовые представления с кешированием и оптимизацией
@method_decorator(cache_page(60 * 30), name='dispatch')  # Кеширование на 30 минут
class ServiceListView(ListView):
    """
    Список всех активных услуг с оптимизированными запросами
    Время загрузки: < 3 секунды
    Поддержка до 50 одновременных пользователей
    """
    model = Service
    template_name = 'services/index.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        # Оптимизация запроса к базе данных для уменьшения времени ответа
        return Service.objects.filter(is_active=True).select_related().order_by('name')
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in ServiceListView: {str(e)}")
            raise

@method_decorator(cache_page(60 * 30), name='dispatch')  # Кеширование на 30 минут
class ServiceDetailView(DetailView):
    """
    Детальная страница услуги с оптимизацией производительности
    Время загрузки: < 3 секунды
    """
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Оптимизация запроса к базе данных
        return Service.objects.select_related()
    
    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            if not obj.is_active:
                raise Http404("Услуга не найдена")
            return obj
        except Service.DoesNotExist:
            logger.warning(f"Service not found: {self.kwargs.get('slug')}")
            raise Http404("Услуга не найдена")
        except Exception as e:
            logger.error(f"Error in ServiceDetailView: {str(e)}")
            raise