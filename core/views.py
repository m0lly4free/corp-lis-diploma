from django.http import HttpResponse
import os

def home_view(request):
    template_path = '/app/templates/home.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse(f"Файл не найден: {template_path}")