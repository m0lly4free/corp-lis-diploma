from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Настройка ролей: Администратор (полный доступ) и Редактор (ограниченный доступ)'

    def handle(self, *args, **kwargs):
        # 1. Группа "Администраторы"
        admin_group, created = Group.objects.get_or_create(name='Администраторы')
        if created:
            all_permissions = Permission.objects.all()
            admin_group.permissions.set(all_permissions)
            self.stdout.write(self.style.SUCCESS('✅ Группа "Администраторы" создана (полный доступ).'))

        # 2. Группа "Редакторы"
        editor_group, created = Group.objects.get_or_create(name='Редакторы')
        if created:
            # Модели, доступные редакторам
            from news.models import News
            from services.models import Service
            from pages.models import Page
            from contacts.models import ContactMessage
            
            allowed_models = [News, Service, Page, ContactMessage]
            permissions_to_add = []

            for model in allowed_models:
                content_type = ContentType.objects.get_for_model(model)
                # Права: добавление, изменение, просмотр (БЕЗ удаления)
                codenames = [
                    f'add_{model._meta.model_name}',
                    f'change_{model._meta.model_name}',
                    f'view_{model._meta.model_name}'
                ]
                perms = Permission.objects.filter(content_type=content_type, codename__in=codenames)
                permissions_to_add.extend(perms)

            editor_group.permissions.set(permissions_to_add)
            self.stdout.write(self.style.SUCCESS('✅ Группа "Редакторы" создана (Новости, Услуги, Страницы, Обращения).'))

        self.stdout.write(self.style.SUCCESS('🎉 Настройка ролей завершена!'))