from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Сохраняем существующий маршрут для совместимости
    path('<slug:slug>/', views.page_view, name='page'),
    
    # Добавляем новый маршрут с кешированием
    path('', views.PageListView.as_view(), name='page_list'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]