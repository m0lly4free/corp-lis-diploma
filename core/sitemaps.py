from django.contrib import sitemaps
from django.urls import reverse, NoReverseMatch
from services.models import Service
from news.models import News
from pages.models import Page
from django.utils import timezone

class StaticViewSitemap(sitemaps.Sitemap):
    """Карта сайта для статических страниц"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        """Возвращает список URL-маршрутов статических страниц"""
        return [
            'core:home',
            'core:about',
            'core:partners',
            'contacts:contact',
            'pages:page_list',
        ]

    def location(self, item):
        """Возвращает URL для статических страниц с обработкой ошибок"""
        try:
            return reverse(item)
        except NoReverseMatch:
            # Если URL не найден, возвращаем корневой URL
            return '/'

class ServiceSitemap(sitemaps.Sitemap):
    """Карта сайта для услуг"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        """Возвращает список активных услуг"""
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        """Возвращает дату последнего обновления услуги"""
        return obj.updated_at

    def location(self, obj):
        """Возвращает URL для услуги с обработкой ошибок"""
        try:
            return reverse('services:detail', kwargs={'slug': obj.slug})
        except NoReverseMatch:
            # Если URL не найден, возвращаем корневой URL
            return '/'

class NewsSitemap(sitemaps.Sitemap):
    """Карта сайта для новостей"""
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        """Возвращает список активных новостей"""
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        """Возвращает дату последнего обновления новости"""
        return obj.updated_at

    def location(self, obj):
        """Возвращает URL для новости с обработкой ошибок"""
        try:
            return reverse('news:detail', kwargs={'slug': obj.slug})
        except NoReverseMatch:
            # Если URL не найден, возвращаем корневой URL
            return '/'

class PageSitemap(sitemaps.Sitemap):
    """Карта сайта для статических страниц"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        """Возвращает список активных страниц"""
        return Page.objects.filter(is_active=True)

    def lastmod(self, obj):
        """Возвращает дату последнего обновления страницы"""
        return obj.updated_at

    def location(self, obj):
        """Возвращает URL для страницы с обработкой ошибок"""
        try:
            return reverse('pages:detail', kwargs={'slug': obj.slug})
        except NoReverseMatch:
            # Если URL не найден, возвращаем корневой URL
            return '/'

class HomePageSitemap(sitemaps.Sitemap):
    """Карта сайта для главной страницы"""
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        """Возвращает главную страницу"""
        return ['core:home']

    def location(self, item):
        """Возвращает URL главной страницы с обработкой ошибок"""
        try:
            return reverse(item)
        except NoReverseMatch:
            return '/'

# Определение карты сайта
sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'news': NewsSitemap,
    'pages': PageSitemap,
    'home': HomePageSitemap,
}