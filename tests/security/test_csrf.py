from django.test import TestCase, Client


class CSRFProtectionTest(TestCase):
    """Проверка CSRF-защиты (9.2.5.1)"""
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
    
    def test_csrf_token_in_forms(self):
        """CSRF-токен присутствует в формах"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'csrfmiddlewaretoken', response.content)
    
    def test_post_without_csrf_fails(self):
        """POST без CSRF-токена отклоняется"""
        response = self.client.post('/contacts/', {
            'name': 'Тест',
            'email': 'test@example.com',
            'phone': '79991234567',
            'message': 'Сообщение'
        })
        # Без CSRF-токена должен быть 403
        self.assertEqual(response.status_code, 403)
    
    def test_csrf_token_validation(self):
        """Валидный CSRF-токен позволяет отправить форму"""
        # Получаем токен
        get_response = self.client.get('/contacts/')
        csrf_token = get_response.cookies.get('csrftoken')
        
        if csrf_token:
            # Отправляем форму с токеном
            response = self.client.post('/contacts/', {
                'name': 'Тест',
                'email': 'test@example.com',
                'phone': '79991234567',
                'message': 'Сообщение',
                'csrfmiddlewaretoken': csrf_token.value
            }, HTTP_REFERER='http://testserver/contacts/')
            
            # Успешная отправка: 302 (редирект) или 200 с сообщением
            self.assertIn(response.status_code, [200, 302])