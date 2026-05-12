from django.test import TestCase, Client
from services.models import Service
from news.models import News


class UserFlowsTest(TestCase):
    """Тестирование пользовательских сценариев (9.2.2)"""
    
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name='Покупка лома',
            slug='purchase',
            short_description='Описание',
            description='Текст'
        )
        self.news = News.objects.create(
            title='Новость',
            slug='news-1',
            short_description='Кратко',
            content='Полный текст'
        )
    
    def test_homepage_loads(self):
        """Сценарий: пользователь открывает главную"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'АО «Корпорация ЛИС»')
    
    def test_browse_services(self):
        """Сценарий: просмотр каталога услуг"""
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Покупка лома')
    
    def test_view_service_detail(self):
        """Сценарий: переход к детальной странице услуги"""
        response = self.client.get(f'/services/{self.service.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Покупка лома')
    
    def test_read_news(self):
        """Сценарий: чтение новости"""
        response = self.client.get(f'/news/{self.news.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новость')
    
    def test_submit_contact_form(self):
        """Сценарий: отправка формы обратной связи"""
        response = self.client.post('/contacts/', {
            'name': 'Тестовый пользователь',
            'email': 'test@example.com',
            'phone': '79991234567',
            'message': 'Тестовое сообщение'
        }, follow=True)
        # После отправки должен быть редирект или сообщение
        self.assertEqual(response.status_code, 200)