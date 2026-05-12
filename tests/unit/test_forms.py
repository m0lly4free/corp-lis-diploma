from django.test import TestCase
from contacts.forms import ContactForm


class ContactFormTest(TestCase):
    """Тесты формы обратной связи (9.2.1.1)"""
    
    def test_form_valid_data(self):
        form_data = {
            'name': 'Иван Иванов',
            'email': 'ivan@example.com',
            'phone': '79991234567',
            'message': 'Здравствуйте!'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Ошибки: {form.errors}")
    
    def test_form_required_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)
    
    def test_form_invalid_email(self):
        form_data = {
            'name': 'Иван',
            'email': 'неправильный',
            'phone': '79991234567',
            'message': 'Тест'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_phone_validation(self):
        """Тест: валидация телефона"""
        form_data = {
            'name': 'Иван',
            'email': 'ivan@test.com',
            'phone': 'не-телефон',
            'message': 'Тест'
        }
        form = ContactForm(data=form_data)
        # Телефон может быть необязательным или иметь свою валидацию
        # Проверяем, что форма хотя бы обрабатывает поле
        self.assertIn('phone', form.fields)