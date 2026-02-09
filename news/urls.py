from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.news_list_view, name="list"),
    path("<int:pk>/", views.news_detail_view, name="detail"),
]