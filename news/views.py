from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import News
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# Функциональное представление для списка новостей (для совместимости)
@cache_page(60 * 30)  # Кэширование на 30 минут
def news_list(request):
    """Страница списка всех новостей с оптимизацией производительности"""
    try:
        # Оптимизация запроса к базе данных для уменьшения времени ответа
        news_list = News.objects.filter(is_active=True).select_related().order_by('-created_at')
        context = {
            'news': news_list,
        }
        return render(request, 'news/index.html', context)
    except Exception as e:
        logger.error(f"Error in news_list: {str(e)}")
        raise

# Функциональное представление для детальной страницы новости (для совместимости)
@cache_page(60 * 30)  # Кэширование на 30 минут
def news_detail(request, slug):
    """Страница конкретной новости с оптимизацией производительности"""
    try:
        news_item = get_object_or_404(News, slug=slug, is_active=True)
        context = {
            'object': news_item,
        }
        return render(request, 'news/detail.html', context)
    except Http404:
        logger.warning(f"News not found: {slug}")
        raise
    except Exception as e:
        logger.error(f"Error in news_detail: {str(e)}")
        raise

# Классовые представления с кешированием и оптимизацией
@method_decorator(cache_page(60 * 30), name='dispatch')  # Кеширование на 30 минут
class NewsListView(ListView):
    """
    Список всех активных новостей с оптимизированными запросами
    Время загрузки: < 3 секунды
    Поддержка до 50 одновременных пользователей
    """
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        # Оптимизация запроса к базе данных для уменьшения времени ответа
        return News.objects.filter(is_active=True).select_related().order_by('-created_at')
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in NewsListView: {str(e)}")
            raise

@method_decorator(cache_page(60 * 30), name='dispatch')  # Кеширование на 30 минут
class NewsDetailView(DetailView):
    """
    Детальная страница конкретной новости с оптимизацией производительности
    Время загрузки: < 3 секунды
    """
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'object'  # Используем 'object' для совместимости с шаблонами
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Оптимизация запроса к базе данных
        return News.objects.select_related()
    
    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            if not obj.is_active:
                raise Http404("Новость не найдена")
            return obj
        except News.DoesNotExist:
            logger.warning(f"News not found: {self.kwargs.get('slug')}")
            raise Http404("Новость не найдена")
        except Exception as e:
            logger.error(f"Error in NewsDetailView: {str(e)}")
            raise