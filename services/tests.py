from django.test import TestCase
from django.core.exceptions import ValidationError
from services.models import Service
from django.utils.text import slugify


class ServiceModelTest(TestCase):
    """Тесты для модели Service"""
    
    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных (выполняется один раз для всех тестов)"""
        cls.service = Service.objects.create(
            name='Покупка лома',
            slug='purchase-scrap',
            short_description='Краткое описание услуги',
            description='Полное описание услуги покупки лома',
            is_active=True
        )
    
    def test_service_creation(self):
        """Тест: услуга создаётся корректно"""
        self.assertEqual(self.service.name, 'Покупка лома')
        self.assertEqual(self.service.slug, 'purchase-scrap')
        self.assertTrue(self.service.is_active)
    
    def test_service_str_method(self):
        """Тест: метод __str__ возвращает название услуги"""
        self.assertEqual(str(self.service), 'Покупка лома')
    
    def test_service_slug_auto_generation(self):
        """Тест: slug генерируется автоматически из name, если не указан"""
        service = Service.objects.create(
            name='Демонтаж зданий',
            short_description='Описание',
            description='Полное описание'
        )
        expected_slug = slugify('Демонтаж зданий')
        self.assertEqual(service.slug, expected_slug)
    
    def test_service_unique_slug(self):
        """Тест: slug должен быть уникальным"""
        with self.assertRaises(Exception):
            Service.objects.create(
                name='Другая услуга',
                slug='purchase-scrap',  # Дубликат существующего
                short_description='Описание',
                description='Полное описание'
            )
    
    def test_service_required_fields(self):
        """Тест: обязательные поля не могут быть пустыми"""
        service = Service(name='')
        with self.assertRaises(ValidationError):
            service.full_clean()  # Запускает валидацию модели
    
    def test_service_get_absolute_url(self):
        """Тест: метод get_absolute_url возвращает корректный URL"""
        expected_url = f'/services/{self.service.slug}/'
        self.assertEqual(self.service.get_absolute_url(), expected_url)
    
    def test_service_filter_active(self):
        """Тест: менеджер active возвращает только активные услуги"""
        inactive = Service.objects.create(
            name='Неактивная услуга',
            slug='inactive-service',
            short_description='Описание',
            description='Полное описание',
            is_active=False
        )
        active_services = Service.objects.filter(is_active=True)
        self.assertIn(self.service, active_services)
        self.assertNotIn(inactive, active_services)