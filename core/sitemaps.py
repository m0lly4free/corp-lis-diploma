from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Page
from services.models import Service
from news.models import News

class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'contacts:contact']

    def location(self, item):
        return reverse(item)

class PageSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class ServiceSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class NewsSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return obj.updated_at