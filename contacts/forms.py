from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500", "placeholder": "+7 (999) 123-45-67"}
            ),
            "message": forms.Textarea(
                attrs={"class": "w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500", "rows": 5}
            ),
        }