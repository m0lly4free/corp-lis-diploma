from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Сохраняем существующие маршруты для совместимости
    path('all/', views.services_list, name='all'),
    path('<slug:slug>/', views.service_detail, name='detail'),
    
    # Добавляем новые маршруты с кешированием
    path('', views.ServiceListView.as_view(), name='index'),
]