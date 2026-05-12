from django.test import TestCase, Client


class MobileUITest(TestCase):
    """Тестирование UI на мобильных устройствах (9.2.6.2–9.2.6.3)"""
    
    def setUp(self):
        self.client = Client()
        self.mobile_headers = {
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36'
        }
    
    def test_text_readability_mobile(self):
        """Читаемость текста на мобильных"""
        response = self.client.get('/about/', **self.mobile_headers)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        
        # Проверяем наличие стилей для шрифтов
        self.assertTrue('font-size' in content or 'rem' in content)
    
    def test_images_responsive(self):
        """Адаптивность изображений"""
        response = self.client.get('/services/', **self.mobile_headers)
        content = response.content.decode('utf-8')
        
        # Проверяем наличие адаптивных атрибутов
        self.assertTrue(
            'srcset' in content or
            'object-fit' in content or
            'max-width:100%' in content or
            'max-width: 100%' in content
        )
    
    def test_form_inputs_mobile_friendly(self):
        """Формы удобны для мобильных"""
        response = self.client.get('/contacts/', **self.mobile_headers)
        content = response.content.decode('utf-8')
        
        # Проверяем наличие viewport
        self.assertIn('viewport', content)
        # Проверяем наличие полей ввода
        self.assertTrue('type="email"' in content or 'type="tel"' in content)
    
    def test_navigation_mobile(self):
        """Навигация работает на мобильных"""
        response = self.client.get('/', **self.mobile_headers)
        content = response.content.decode('utf-8')
        
        # Проверяем наличие навигации
        self.assertIn('nav', content.lower())