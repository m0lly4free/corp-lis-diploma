from django import forms
from django.utils.translation import gettext_lazy as _
import time
import re

class HoneypotFormMixin(forms.Form):
    """Миксин для добавления honeypot поля с улучшенной защитой"""
    
    hp_email = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none !important;',
            'autocomplete': 'off',
            'id': 'hp_email'
        })
    )
    
    timestamp = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    hp_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none !important;',
            'autocomplete': 'off',
            'id': 'hp_name'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        if cleaned_data.get('hp_email') or cleaned_data.get('hp_name'):
            raise forms.ValidationError(
                _('Сообщение заблокировано как спам.'),
                code='honeypot_detected'
            )
        
        timestamp = cleaned_data.get('timestamp')
        if timestamp:
            current_time = int(time.time())
            if current_time - timestamp < 3:
                raise forms.ValidationError(
                    _('Сообщение отправлено слишком быстро. Пожалуйста, подождите несколько секунд.'),
                    code='too_fast'
                )
        
        message = cleaned_data.get('message', '')
        if len(message) > 0 and len(re.findall(r'http[s]?://|www\.', message)) > 2:
            raise forms.ValidationError(
                _('Сообщение содержит слишком много ссылок.'),
                code='too_many_links'
            )
        
        return cleaned_data

class ContactForm(HoneypotFormMixin, forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(
        max_length=255,
        label=_('Имя'),
        widget=forms.TextInput(attrs={'placeholder': _('Ваше имя')})
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'placeholder': _('your@email.com')})
    )
    phone = forms.CharField(
        max_length=50,
        label=_('Телефон'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('+7 (999) 123-45-67')})
    )
    message = forms.CharField(
        label=_('Сообщение'),
        widget=forms.Textarea(attrs={
            'placeholder': _('Ваше сообщение...'),
            'rows': 5
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('timestamp'):
            self.fields['timestamp'].initial = int(time.time())
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise forms.ValidationError(_('Имя должно содержать минимум 2 символа.'))
        return name
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message.strip()) < 10:
            raise forms.ValidationError(_('Сообщение должно содержать минимум 10 символов.'))
        return message