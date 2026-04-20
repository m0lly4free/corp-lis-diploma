from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserRole

class UserRoleInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    verbose_name = 'Роль'
    verbose_name_plural = 'Роли'

class UserAdmin(BaseUserAdmin):
    """
    Расширенная админ-панель для управления пользователями
    Соответствует требованиям ТЗ 3.2.6
    """
    
    # 1. Просмотр всех пользователей
    list_display = ('username', 'email', 'role_display', 'is_active_status', 'date_joined', 'last_login')
    list_display_links = ('username',)
    
    # 5. Фильтр по ролям и статусу
    list_filter = ('user_role__role', 'is_active', 'date_joined', 'last_login')
    
    # Поиск по основным полям
    search_fields = ('username', 'email', 'first_name', 'last_name')
    search_help_text = 'Поиск по имени пользователя, email, имени и фамилии'
    
    # Поля формы создания/редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    
    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # Параметры отображения
    ordering = ['-date_joined']
    list_per_page = 20
    
    # Добавляем inline для роли
    inlines = [UserRoleInline]
    
    # 1. Отображение роли в списке
    def role_display(self, obj):
        try:
            role = obj.user_role.role
            if role == 'admin':
                return format_html('<span style="color: #d9534f; font-weight: bold;">Администратор</span>')
            elif role == 'editor':
                return format_html('<span style="color: #5bc0de; font-weight: bold;">Редактор</span>')
            else:
                return '-'
        except UserRole.DoesNotExist:
            return '-'
    role_display.short_description = 'Роль'
    role_display.admin_order_field = 'user_role__role'
    
    # 1. Отображение статуса активности
    def is_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Активен</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Неактивен</span>')
    is_active_status.short_description = 'Статус'
    is_active_status.admin_order_field = 'is_active'
    
    # 6. Логирование действий пользователей
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Создаем запись о роли, если она не существует
        if not hasattr(obj, 'user_role'):
            UserRole.objects.create(user=obj)
        
        # Логирование действий
        action = "обновлен" if change else "создан"
        print(f"Пользователь {obj.username} был {action} администратором {request.user.username}")

# Отменяем регистрацию стандартной модели User
admin.site.unregister(User)
# Регистрируем с нашим расширением
admin.site.register(User, UserAdmin)