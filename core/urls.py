from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', include('services.urls', namespace='services')),




]

urlpatterns += [
    re_path(r'^about/static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),
]