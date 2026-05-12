from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Service
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# ==========================================
# Функциональные представления (для совместимости)
# ==========================================
@cache_page(60 * 30)  # Кэширование на 30 минут
def services_list(request):
    """Страница списка всех услуг с оптимизацией производительности"""
    try:
        services = Service.objects.filter(is_active=True).order_by('name')
        
        return render(request, 'services/index.html', {'services': services})
    except Exception as e:
        logger.error(f"Error in services_list: {str(e)}")
        raise

@cache_page(60 * 30)  # Кэширование на 30 минут
def service_detail(request, slug):
    """Страница конкретной услуги с оптимизацией производительности"""
    try:
        service = get_object_or_404(Service, slug=slug, is_active=True)
        return render(request, 'services/detail.html', {'service': service})
    except Http404:
        logger.warning(f"Service not found: {slug}")
        raise
    except Exception as e:
        logger.error(f"Error in service_detail: {str(e)}")
        raise

# ==========================================
# Классовые представления (основные, ТЗ 4.4)
# ==========================================
@method_decorator(cache_page(60 * 30), name='dispatch')
class ServiceListView(ListView):
    """
    Список всех активных услуг с пагинацией и оптимизированными запросами.
    Время загрузки: < 3 секунды
    Поддержка до 50 одновременных пользователей (обеспечено paginate_by)
    """
    model = Service
    template_name = 'services/index.html'
    context_object_name = 'services'
    paginate_by = 10  #  Важно для нагрузки: ограничивает выборку
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by('name')

@method_decorator(cache_page(60 * 30), name='dispatch')
class ServiceDetailView(DetailView):
    """
    Детальная страница услуги с оптимизацией производительности.
    Время загрузки: < 3 секунды
    """
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Оптимизация: Фильтруем только активные услуги.
        # Если есть ForeignKey, добавьте сюда .select_related('category')
        return Service.objects.filter(is_active=True)
    
    def get_object(self, queryset=None):
        # Django автоматически вызовет super().get_object(queryset)
        # Если объект не найден (включая is_active=False), Django вернет 404
        try:
            return super().get_object(queryset)
        except Service.DoesNotExist:
            logger.warning(f"Service not found: {self.kwargs.get('slug')}")
            raise Http404("Услуга не найдена")