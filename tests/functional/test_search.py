from django.test import TestCase, Client
from services.models import Service


class SearchFunctionalityTest(TestCase):
    """Проверка поиска (9.2.3.2)"""
    
    def setUp(self):
        self.client = Client()
        Service.objects.create(
            name='Покупка черного лома',
            slug='black-scrap',
            short_description='Описание',
            description='Текст'
        )
        Service.objects.create(
            name='Покупка цветного лома',
            slug='color-scrap',
            short_description='Описание',
            description='Текст'
        )
    
    def test_search_by_keyword(self):
        """Поиск по ключевому слову"""
        response = self.client.get('/services/?q=черного')
        self.assertEqual(response.status_code, 200)
        # Проверяем, что страница загрузилась
        self.assertContains(response, 'услуг', status_code=200)
    
    def test_search_no_results(self):
        """Поиск без результатов"""
        response = self.client.get('/services/?q=несуществующий-запрос')
        self.assertEqual(response.status_code, 200)
        # Страница должна загрузиться, даже если ничего не найдено