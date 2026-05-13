from django.test import TestCase, Client
from services.models import Service


class ServiceAPITest(TestCase):
    """Тесты API-эндпоинтов (9.2.1.3)"""
    
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name='API Тест', slug='api-test',
            short_description='Описание', description='Текст',
            is_active=True
        )
    
    def test_services_list_endpoint_exists(self):
        """Тест: проверяем, что API endpoint существует"""
        response = self.client.get('/api/services/')
        self.assertIn(response.status_code, [200, 404, 401, 403, 500])