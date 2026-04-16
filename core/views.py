from django.http import HttpResponse
from django.shortcuts import render
import os

def home_view(request):
    template_path = '/app/templates/home.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")
    
def about_view(request):
    template_path = '/app/templates/about.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")
    
def partners_view(request):
    template_path = '/app/templates/partners.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")

def contacts_view(request):
    template_path = '/app/templates/contacts.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")
    

    




    

    
