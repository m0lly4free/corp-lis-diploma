from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from axes.decorators import axes_dispatch
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import (
    StaticViewSitemap, 
    ServiceSitemap, 
    NewsSitemap, 
    PageSitemap
)
from django.views.generic import TemplateView
from django.urls import get_resolver

# Определение карты сайта
sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'news': NewsSitemap,
    'pages': PageSitemap,
}

admin.site.login = axes_dispatch(admin.site.login)
app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', include('services.urls', namespace='services')),
    path('news/', include('news.urls', namespace='news')),
    path('partners/', views.partners_view, name='partners'),
    path('contacts/', include('contacts.urls', namespace='contacts')),
    path('page/', include('pages.urls', namespace='pages')),
    path('api/', include('api.urls', namespace='api')),

     # SEO материалы
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='seo/robots.txt', content_type='text/plain'), name='robots_txt'),

]

urlpatterns += [
    re_path(r'^about/static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def check_sitemaps():
    """Проверка регистрации namespace для sitemap"""
    resolver = get_resolver()
    namespaces = resolver.urlconf_module.__dict__.get('urlpatterns', [])
    print("Registered namespaces:", [ns for ns in namespaces if hasattr(ns, 'namespace')])
    
# Вызовите проверку при старте
if __name__ == '__main__':
    check_sitemaps()