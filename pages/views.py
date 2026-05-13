from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Page
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# ==========================================
# Функциональное представление (для обратной совместимости)
# ==========================================
@cache_page(60 * 60)  # 1 час кэширования (статические страницы меняются редко)
def page_view(request, slug):
    """Страница конкретной статической страницы"""
    try:
        # get_object_or_404 уже оптимизирован под Django ORM
        page = get_object_or_404(Page.objects.filter(is_active=True), slug=slug)
        return render(request, 'pages/page.html', {'page': page})
    except Http404:
        logger.warning(f"Page not found: {slug}")
        raise
    except Exception as e:
        logger.error(f"Error in page_view: {str(e)}")
        raise

# ==========================================
# Классовые представления (основные, ТЗ 4.4)
# ==========================================
@method_decorator(cache_page(60 * 60), name='dispatch')
class PageListView(ListView):
    """
    Список статических страниц с пагинацией.
    Пагинация критична для стабильности при высокой нагрузке (ТЗ 4.4.1).
    """
    model = Page
    template_name = 'pages/list.html'
    context_object_name = 'pages'
    paginate_by = 20 
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True).order_by('title')

@method_decorator(cache_page(60 * 60), name='dispatch')
class PageDetailView(DetailView):
    """
    Детальная страница с кэшированием и проверкой статуса.
    """
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if not obj.is_active:
            raise Http404("Страница не найдена")
        return obj