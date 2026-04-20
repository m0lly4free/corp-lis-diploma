from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from axes.decorators import axes_dispatch

admin.site.login = axes_dispatch(admin.site.login)
app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', include('services.urls', namespace='services')),
    path('news/', include('news.urls', namespace='news')),
    path('partners/', views.partners_view, name='partners'),
    path('contacts/', include('contacts.urls', namespace='contact')),
    path('page/', include('pages.urls', namespace='pages')),





]

urlpatterns += [
    re_path(r'^about/static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)