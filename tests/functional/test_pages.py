from django.test import TestCase, Client


class PageAvailabilityTest(TestCase):
    """Проверка доступности всех страниц (9.2.3.1)"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page_status(self):
        """Главная страница возвращает 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_page_status(self):
        """Страница 'О компании' возвращает 200"""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_services_list_status(self):
        """Список услуг возвращает 200"""
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
    
    def test_news_list_status(self):
        """Список новостей возвращает 200"""
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
    
    def test_contacts_page_status(self):
        """Страница контактов возвращает 200"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
    
    def test_404_for_nonexistent_page(self):
        """Несуществующая страница возвращает 404"""
        response = self.client.get('/nonexistent-page-12345/')
        self.assertEqual(response.status_code, 404)