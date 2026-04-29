from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import News
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# ==========================================
# Функциональные представления (совместимость)
# ==========================================
@cache_page(60 * 15)  # 15 минут
def news_list(request):
    """Список новостей с оптимизированными запросами"""
    try:
        # ✅ Убраны select_related/prefetch_related — в модели News нет ForeignKey
        news_list = News.objects.filter(is_active=True).order_by('-created_at')
        return render(request, 'news/index.html', {'news': news_list})
    except Exception as e:
        logger.error(f"Error in news_list: {str(e)}")
        raise

@cache_page(60 * 30)  # 30 минут
def news_detail(request, slug):
    """Детальная страница новости"""
    try:
        news_item = get_object_or_404(News, slug=slug, is_active=True)
        return render(request, 'news/detail.html', {'object': news_item})
    except Http404:
        logger.warning(f"News not found: {slug}")
        raise
    except Exception as e:
        logger.error(f"Error in news_detail: {str(e)}")
        raise

# ==========================================
# Классовые представления (основные, ТЗ 4.4)
# ==========================================
@method_decorator(cache_page(60 * 15), name='dispatch')
class NewsListView(ListView):
    """
    Список новостей с пагинацией и оптимизацией ORM.
    paginate_by снижает нагрузку на БД и память при больших выборках.
    """
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 12  # Рекомендуется для стабильности при 50+ юзерах
    
    def get_queryset(self):
        # ✅ Убраны select_related/prefetch_related — в модели нет ForeignKey
        return News.objects.filter(is_active=True).order_by('-created_at')

@method_decorator(cache_page(60 * 30), name='dispatch')
class NewsDetailView(DetailView):
    """Детальная страница с кэшированием и проверкой статуса"""
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'object'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # ✅ Оптимизация для одиночного объекта — без select_related
        return News.objects.filter(is_active=True)
    
    def get_object(self, queryset=None):
        # Django сам вызывает get_object с переданным queryset
        obj = super().get_object(queryset)
        if not obj.is_active:
            raise Http404("Новость не найдена")
        return obj