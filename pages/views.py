from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Page

# Функциональное представление для страниц (для совместимости)
def page_view(request, slug):
    """Страница конкретной статической страницы"""
    page = get_object_or_404(Page, slug=slug, is_active=True)
    context = {
        'page': page,
    }
    return render(request, 'pages/page.html', context)

# Классовые представления с кешированием
@method_decorator(cache_page(60 * 60), name='dispatch')  # Кеширование на 1 час
class PageListView(ListView):
    """
    Список всех активных статических страниц с оптимизированными запросами
    """
    model = Page
    template_name = 'pages/list.html'
    context_object_name = 'pages'
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True).select_related().order_by('title')

class PageDetailView(DetailView):
    """
    Детальная страница конкретной статической страницы с оптимизированными запросами
    """
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Page.objects.select_related()