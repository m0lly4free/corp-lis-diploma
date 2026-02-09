from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contact_view, name="contact"),
    path("api/", views.ContactMessageCreateView.as_view(), name="contact-api"),
]