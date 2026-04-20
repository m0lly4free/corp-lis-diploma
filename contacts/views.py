from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем в базу данных
            contact_message = form.save(commit=False)
            contact_message.is_processed = False  # Новое обращение
            contact_message.save()
            
            # Отправляем сообщение пользователю
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return render(request, 'contacts.html', {'form': form})
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()
    
    return render(request, 'contacts.html', {'form': form})