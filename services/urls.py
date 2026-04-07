from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='index'),
    path('all/', views.services_list, name='all'),
    path('<slug:slug>/', views.service_detail, name='detail'),
]