from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    """Страница списка новостей"""
    news = News.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'news': news,
    }
    return render(request, 'news/index.html', context)

def news_detail(request, slug):
    """Страница конкретной новости"""
    news = get_object_or_404(News, slug=slug, is_active=True)
    context = {
        'news': news,
    }
    return render(request, 'news/detail.html', context)