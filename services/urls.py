from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.services_list_view, name="list"),
    path("<int:pk>/", views.service_detail_view, name="detail"),
]