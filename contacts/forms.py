from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ваш email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ваш телефон'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Напишите ваше сообщение',
                'rows': 5
            }),
        }