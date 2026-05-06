import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from services.models import Service
from news.models import News

@login_required
def protected_media(request, path):
    """
    Защищенный доступ к медиафайлам только для авторизованных пользователей
    """
    # Проверка пути на безопасность
    if '..' in path or path.startswith('/'):
        raise Http404("Недопустимый путь")
    
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(file_path):
        raise Http404("Файл не найден")
    
    # Чтение файла и отправка ответа
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    
def home_view(request):
    template_path = '/app/templates/home.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")
    
def about_view(request):
    template_path = '/app/templates/about.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")
    
def partners_view(request):
    template_path = '/app/templates/partners.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")

    
def page_view(request, slug):
    template_path = '/app/templates/pages/page.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")
    
@method_decorator(cache_page(60 * 15), name='dispatch')  # Кеширование на 15 минут
class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Оптимизированные запросы с select_related/prefetch_related
        context['services'] = Service.objects.filter(is_active=True).select_related()
        context['news'] = News.objects.filter(is_active=True).select_related()[:5]
        return context

@method_decorator(cache_page(60 * 60), name='dispatch')  # Кеширование на 1 час
class AboutView(TemplateView):
    template_name = 'core/about.html'

@method_decorator(cache_page(60 * 60), name='dispatch')
class PartnersView(TemplateView):
    template_name = 'core/partners.html'
    
import logging
from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound

logger = logging.getLogger('system_errors')

def custom_404(request, exception):
    """Обработчик ошибки 404"""
    logger.warning(f"404 error: {request.path} - {str(exception)}")
    return HttpResponseNotFound(render(request, 'errors/404.html'))

def custom_500(request):
    """Обработчик ошибки 500"""
    logger.error(f"500 error: {request.path}")
    return HttpResponseServerError(render(request, 'errors/500.html'))

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(TemplateView):
    """
    Главная страница с динамическими услугами и новостями.
    Кэшируется на 15 минут для снижения нагрузки на БД.
    """
    # Правильный путь к шаблону (без папки core/)
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 3 последние активные услуги
        context['latest_services'] = Service.objects.filter(
            is_active=True
        ).order_by('-created_at')[:3]
        
        # 3 последние активные новости
        context['latest_news'] = News.objects.filter(
            is_active=True
        ).order_by('-created_at')[:3]
        
        return context
    




    

    
