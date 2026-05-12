from django.test import TestCase, Client
from services.models import Service


class XSSProtectionTest(TestCase):
    """Проверка защиты от XSS (9.2.5.2)"""
    
    def setUp(self):
        self.client = Client()
    
    def test_script_tag_escaped_in_content(self):
        """Тест: скрипты экранируются в контенте (не в <style>)"""
        malicious_content = '<script>alert("XSS")</script>'
        service = Service.objects.create(
            name='Тест', slug='xss-test',
            short_description='Безопасное описание',
            description=malicious_content
        )
        
        response = self.client.get(f'/services/{service.slug}/')
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        
        # Находим только контент секции (между <div class="service-description"> и </div>)
        # Или проверяем, что alert не выполняется как JS
        # Django экранирует < и > в &lt; и &gt; в шаблонах
        if '<script>' in content:
            # Если <script> есть, проверяем, что он внутри <style> или экранирован
            # Ищем вхождение вне тегов <style> и <script>
            import re
            # Удаляем блоки <style>...</style> из проверки
            content_no_style = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
            # Теперь проверяем
            self.assertNotIn('<script>alert', content_no_style, 
                           "XSS-скрипт не экранирован в контенте!")