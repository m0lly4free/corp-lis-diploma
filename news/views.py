from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import News

# Классовые представления с кешированием
@method_decorator(cache_page(60 * 10), name='dispatch')  # Кеширование на 10 минут
class NewsListView(ListView):
    """
    Список всех активных новостей с оптимизированными запросами
    """
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        # Оптимизация запроса с select_related для уменьшения количества SQL-запросов
        return News.objects.filter(is_active=True).select_related().order_by('-created_at')

class NewsDetailView(DetailView):
    """
    Детальная страница конкретной новости с оптимизированными запросами
    """
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Оптимизация запроса с select_related для уменьшения количества SQL-запросов
        return News.objects.select_related()