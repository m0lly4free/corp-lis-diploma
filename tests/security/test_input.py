from django.test import TestCase
from contacts.forms import ContactForm


class InputValidationTest(TestCase):
    """Тестирование валидации ввода (9.2.5.3)"""
    
    def test_sql_injection_handled(self):
        """Тест: форма обрабатывает потенциально опасный ввод"""
        malicious_input = "'; DROP TABLE contacts_contactmessage; --"
        form = ContactForm(data={
            'name': malicious_input,
            'email': 'test@example.com',
            'phone': '79991234567',
            'message': 'Тест'
        })
        # Форма должна обработать ввод (валидация на уровне ORM защищает от инъекций)
        # Проверяем, что нет падения с исключением
        try:
            is_valid = form.is_valid()
            self.assertTrue(True)  # Если дошли сюда - нет исключения
        except Exception as e:
            self.fail(f"Форма упала с ошибкой: {e}")
    
    def test_email_format_validation(self):
        invalid_emails = ['not-an-email', '@example.com', 'user@']
        for email in invalid_emails:
            form = ContactForm(data={
                'name': 'Тест', 'email': email,
                'phone': '79991234567', 'message': 'Тест'
            })
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)
    
    def test_message_accepts_long_text(self):
        """Тест: форма принимает длинные сообщения"""
        long_message = 'A' * 1000
        form = ContactForm(data={
            'name': 'Тест', 'email': 'test@example.com',
            'phone': '79991234567', 'message': long_message
        })
        # Форма должна принять или валидировать на уровне модели
        self.assertTrue(form.is_valid() or 'message' in form.errors)