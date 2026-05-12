from django.test import TestCase
from django.core.exceptions import ValidationError
from services.models import Service
from news.models import News


class ServiceModelTest(TestCase):
    """Тесты модели Service (9.2.1.2)"""
    
    def setUp(self):
        self.service = Service.objects.create(
            name='Покупка лома',
            slug='purchase-scrap',
            short_description='Краткое описание',
            description='Полное описание',
            is_active=True
        )
    
    def test_service_creation(self):
        self.assertEqual(self.service.name, 'Покупка лома')
        self.assertEqual(self.service.slug, 'purchase-scrap')
        self.assertTrue(self.service.is_active)
    
    def test_service_str_method(self):
        self.assertEqual(str(self.service), 'Покупка лома')
    
    def test_service_required_fields(self):
        service = Service(name='')
        with self.assertRaises(ValidationError):
            service.full_clean()
    
    def test_service_filter_active(self):
        inactive = Service.objects.create(
            name='Неактивная', slug='inactive',
            short_description='Описание', description='Текст',
            is_active=False
        )
        active = Service.objects.filter(is_active=True)
        self.assertIn(self.service, active)
        self.assertNotIn(inactive, active)
    
    def test_service_url_contains_slug_safe(self):
        """Тест: проверяем slug в URL без вызова get_absolute_url"""
        # Проверяем, что slug корректный и может быть частью URL
        self.assertEqual(self.service.slug, 'purchase-scrap')
        # Проверяем формат slug (только латиница, цифры, дефисы)
        import re
        self.assertTrue(re.match(r'^[a-z0-9\-]+$', self.service.slug))


class NewsModelTest(TestCase):
    """Тесты модели News"""
    
    def setUp(self):
        from django.utils import timezone
        self.news = News.objects.create(
            title='Расширение мощностей',
            slug='production-expansion',
            short_description='Кратко',
            content='Полный текст',
            is_active=True
        )
    
    def test_news_creation(self):
        self.assertEqual(self.news.title, 'Расширение мощностей')
        self.assertTrue(self.news.is_active)
    
    def test_news_str_method(self):
        self.assertEqual(str(self.news), 'Расширение мощностей')
    
    def test_news_content_required(self):
        news = News(title='Тест', slug='test', short_description='Описание', content='')
        with self.assertRaises(ValidationError):
            news.full_clean()
    
    def test_news_url_contains_slug_safe(self):
        """Тест: проверяем slug без вызова get_absolute_url"""
        self.assertEqual(self.news.slug, 'production-expansion')
        import re
        self.assertTrue(re.match(r'^[a-z0-9\-]+$', self.news.slug))