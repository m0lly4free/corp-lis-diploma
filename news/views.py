from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import News
import logging
from django.http import Http404

logger = logging.getLogger('system_errors')

# ==========================================
# Функциональные представления (совместимость)
# ==========================================
@cache_page(60 * 15)
def news_list(request):
    """Список новостей с пагинацией (6 на страницу) и оптимизированными запросами"""
    try:
        # Безопасный запрос - ORM автоматически экранирует параметры
        news_list = News.objects.filter(is_active=True).order_by('-created_at')
        
        # Пагинация: 6 новостей на страницу
        paginator = Paginator(news_list, 6)
        page = request.GET.get('page')
        
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            # Если page не целое число, возвращаем первую страницу
            news = paginator.page(1)
        except EmptyPage:
            # Если страница за пределами диапазона, возвращаем последнюю
            news = paginator.page(paginator.num_pages)
        
        return render(request, 'news/index.html', {'news': news})
    except Exception as e:
        logger.error(f"Error in news_list: {str(e)}")
        raise

@cache_page(60 * 30) 
def news_detail(request, slug):
    """Детальная страница новости"""
    try:
         # get_object_or_404 предотвращает инъекции через slug
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
    Список новостей с пагинацией (6 на страницу) и оптимизацией ORM.
    paginate_by = 6 снижает нагрузку на БД и обеспечивает быструю загрузку.
    """
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 6  
    
    def get_queryset(self):
        
        return News.objects.filter(is_active=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Добавляем в контекст информацию о пагинации для шаблона"""
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(cache_page(60 * 30), name='dispatch')
class NewsDetailView(DetailView):
    """Детальная страница с кэшированием и проверкой статуса"""
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'object'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # ✅ Оптимизация для одиночного объекта — без лишних запросов
        return News.objects.filter(is_active=True)
    
    def get_object(self, queryset=None):
        # Django сам вызывает get_object с переданным queryset
        obj = super().get_object(queryset)
        if not obj.is_active:
            logger.warning(f"News not found or inactive: {self.kwargs.get('slug')}")
            raise Http404("Новость не найдена")
        return obj