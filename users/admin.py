from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UserRole

class UserRoleInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    verbose_name = _('Роль')
    verbose_name_plural = _('Роли')
    classes = ('collapse',)  # Сворачиваем блок по умолчанию

class UserAdmin(BaseUserAdmin):
    """
    Расширенная админ-панель для управления пользователями
    Соответствует требованиям ТЗ 3.2.6 и 3.2.10
    """
    
    # 1. Просмотр всех пользователей
    list_display = ('username', 'email', 'role_display', 'is_active_status', 'date_joined', 'last_login')
    list_display_links = ('username',)
    
    # 5. Фильтр по ролям и статусу
    list_filter = ('user_role__role', 'is_active', 'date_joined', 'last_login')
    
    # Поиск по основным полям
    search_fields = ('username', 'email', 'first_name', 'last_name')
    search_help_text = _('Поиск по имени пользователя, email, имени и фамилии')
    
    # Поля формы создания/редактирования
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('username', 'password'),
            'classes': ('wide',)
        }),
        (_('Персональная информация'), {
            'fields': ('first_name', 'last_name', 'email'),
            'classes': ('wide',)
        }),
        (_('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('wide',)
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('wide',)
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
    
    # Оптимизация запросов
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_role')
    
    # 1. Отображение роли в списке
    def role_display(self, obj):
        try:
            role = obj.user_role.role
            if role == 'admin':
                return format_html('<span style="color: #d9534f; font-weight: bold;">{}</span>', _('Администратор'))
            elif role == 'editor':
                return format_html('<span style="color: #5bc0de; font-weight: bold;">{}</span>', _('Редактор'))
            else:
                return '-'
        except UserRole.DoesNotExist:
            return '-'
    role_display.short_description = _('Роль')
    role_display.admin_order_field = 'user_role__role'
    
    # 1. Отображение статуса активности
    def is_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ {}</span>', _('Активен'))
        return format_html('<span style="color: red; font-weight: bold;">✗ {}</span>', _('Неактивен'))
    is_active_status.short_description = _('Статус')
    is_active_status.admin_order_field = 'is_active'
    
    # Обработка конфликтов при одновременном редактировании
    def response_change(self, request, obj):
        original_version = request.POST.get('original_version')
        if hasattr(obj, 'user_role') and original_version:
            current_version = str(obj.user_role.version)
            if original_version != current_version:
                messages.warning(
                    request, 
                    _('Данные пользователя были изменены другим администратором. '
                      'Пожалуйста, обновите страницу и внесите изменения снова.')
                )
                return HttpResponseRedirect(reverse('admin:auth_user_change', args=[obj.id]))
        return super().response_change(request, obj)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            if hasattr(obj, 'user_role'):
                extra_context['original_version'] = str(obj.user_role.version)
        return super().change_view(request, object_id, form_url, extra_context)
    
    # 6. Логирование действий пользователей
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Создаем запись о роли, если она не существует
        if not hasattr(obj, 'user_role'):
            UserRole.objects.create(user=obj)
        
        # Логирование действий
        action = _("обновлен") if change else _("создан")
        print(f"Пользователь {obj.username} был {action} администратором {request.user.username}")

# Отменяем регистрацию стандартной модели User
admin.site.unregister(User)
# Регистрируем с нашим расширением
admin.site.register(User, UserAdmin)