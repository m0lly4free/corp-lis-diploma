from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Service

# Функциональное представление для списка услуг (для совместимости)
def services_list(request):
    """Страница списка всех услуг"""
    services = Service.objects.filter(is_active=True).select_related().order_by('name')
    context = {
        'services': services,
    }
    return render(request, 'services/index.html', context)

# Функциональное представление для детальной страницы услуги (для совместимости)
def service_detail(request, slug):
    """Страница конкретной услуги"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {
        'service': service,
    }
    return render(request, 'services/detail.html', context)

# Классовые представления с кешированием
@method_decorator(cache_page(60 * 30), name='dispatch')  # Кеширование на 30 минут
class ServiceListView(ListView):
    """
    Список всех активных услуг с оптимизированными запросами
    """
    model = Service
    template_name = 'services/index.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related().order_by('name')

class ServiceDetailView(DetailView):
    """
    Детальная страница конкретной услуги с оптимизированными запросами
    """
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Service.objects.select_related()