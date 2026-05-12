from django.test import TestCase, Client


class ResponsiveDesignTest(TestCase):
    """Проверка адаптивности блоков (9.2.6.1)"""
    
    def setUp(self):
        self.client = Client()
    
    def test_mobile_user_agent_receives_responsive_html(self):
        """Мобильный User-Agent получает адаптивный HTML"""
        response = self.client.get(
            '/',
            HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
        )
        self.assertEqual(response.status_code, 200)
        
        # Проверяем наличие viewport мета-тега
        content = response.content.decode('utf-8')
        self.assertIn('viewport', content)
    
    def test_desktop_user_agent_receives_full_html(self):
        """Десктопный User-Agent получает полную версию"""
        response = self.client.get(
            '/',
            HTTP_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        )
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        self.assertIn('viewport', content)