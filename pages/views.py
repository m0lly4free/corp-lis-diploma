from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Page
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# Функциональное представление для страниц (для совместимости)
@cache_page(60 * 60)  # Кэширование на 1 час
def page_view(request, slug):
    """Страница конкретной статической страницы с оптимизацией производительности"""
    try:
        page = get_object_or_404(Page, slug=slug, is_active=True)
        context = {
            'page': page,
        }
        return render(request, 'pages/page.html', context)
    except Http404:
        logger.warning(f"Page not found: {slug}")
        raise
    except Exception as e:
        logger.error(f"Error in page_view: {str(e)}")
        raise

# Классовые представления с кешированием и оптимизацией
@method_decorator(cache_page(60 * 60), name='dispatch')  # Кеширование на 1 час
class PageListView(ListView):
    """
    Список всех активных статических страниц с оптимизированными запросами
    Время загрузки: < 3 секунды
    Поддержка до 50 одновременных пользователей
    """
    model = Page
    template_name = 'pages/list.html'
    context_object_name = 'pages'
    
    def get_queryset(self):
        # Оптимизация запроса к базе данных для уменьшения времени ответа
        return Page.objects.filter(is_active=True).select_related().order_by('title')
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in PageListView: {str(e)}")
            raise

@method_decorator(cache_page(60 * 60), name='dispatch')  # Кеширование на 1 час
class PageDetailView(DetailView):
    """
    Детальная страница конкретной статической страницы с оптимизацией производительности
    Время загрузки: < 3 секунды
    """
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Оптимизация запроса к базе данных
        return Page.objects.select_related()
    
    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            if not obj.is_active:
                raise Http404("Страница не найдена")
            return obj
        except Page.DoesNotExist:
            logger.warning(f"Page not found: {self.kwargs.get('slug')}")
            raise Http404("Страница не найдена")
        except Exception as e:
            logger.error(f"Error in PageDetailView: {str(e)}")
            raise