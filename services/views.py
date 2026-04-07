from django.shortcuts import render, get_object_or_404
from .models import Service

def services_list(request):
    """Страница списка услуг"""
    services = Service.objects.filter(is_active=True)
    categories = [
        ('', 'Все услуги'),
        ('purchase', 'Покупка лома'),
        ('dismantling', 'Демонтаж'),
        ('self_transport', 'Самовывоз'),
        ('production', 'Производство'),
        ('sales', 'Продажа'),
        ('consulting', 'Консультации'),
    ]
    
    # Получаем выбранный фильтр
    category = request.GET.get('category', '')
    if category:
        services = services.filter(category=category)
    
    context = {
        'services': services,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'services/index.html', {'services': services})  # Строчные буквы

def service_detail(request, slug):
    """Страница детальной услуги"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {
        'service': service,
    }
    return render(request, 'services/detail.html', context)