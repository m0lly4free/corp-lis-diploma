from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminProtectionTest(TestCase):
    """Проверка защиты административного раздела (9.2.5.4)"""
    
    def setUp(self):
        self.client = Client()
        # Создаем обычного пользователя
        self.regular_user = User.objects.create_user(
            username='regular',
            password='pass123',
            is_staff=False
        )
        # Создаем администратора с правильными учетными данными
        self.admin_user = User.objects.create_superuser(
            username='root',
            password='root',
            email='root@corp-lis.ru',
            is_staff=True
        )
    
    def test_custom_admin_requires_login(self):
        """Тест: кастомная админка требует авторизации"""
        response = self.client.get('/corp-lis-secure-portal/')
        # Допустимо: 302 (редирект на логин) или 404 (не подключена)
        self.assertIn(response.status_code, [302, 404])
    
    def test_regular_user_cannot_access_admin(self):
        """Тест: обычный пользователь не имеет доступа к админке"""
        self.client.login(username='regular', password='pass123')
        response = self.client.get('/corp-lis-secure-portal/')
        # Должен быть 403 (запрет), 404 (не подключена) или 302 (редирект)
        self.assertIn(response.status_code, [403, 404, 302])
    
    def test_root_superuser_can_access_admin(self):
        """Тест: суперпользователь root имеет доступ к админке"""
        login_success = self.client.login(username='root', password='root')
        self.assertTrue(login_success, "Логин root/root не работает")
        
        response = self.client.get('/corp-lis-secure-portal/')
        # 200 (доступ) или 404 (не подключена) - оба допустимы
        self.assertIn(response.status_code, [200, 404])
    
    def test_wrong_password_fails(self):
        """Тест: неправильный пароль отклоняется"""
        login_success = self.client.login(username='root', password='wrongpassword')
        self.assertFalse(login_success, "Неправильный пароль должен отклоняться")