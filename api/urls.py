from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Главная страница
    path('', views.APIRootView.as_view(), name='api-root'),

    # Получение списка услуг
    path('services/', views.ServiceListView.as_view(), name='service-list'),
    
    # Получение конкретной услуги
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service-detail'),
    
    # Получение списка новостей
    path('news/', views.NewsListView.as_view(), name='news-list'),
    
    # Получение конкретной новости
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news-detail'),
    
    # Отправка данных формы обратной связи
    path('contact/', views.ContactMessageCreateView.as_view(), name='contact-create'),
    
    # Получение статической страницы
    path('page/', views.PageListView.as_view(), name='page-list'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
]