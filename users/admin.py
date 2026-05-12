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
    extra = 0  # ← Запрещаем создание дублей ролей
    # Убрали classes=('collapse',) чтобы форма всегда корректно отправлялась

class UserAdmin(BaseUserAdmin):
    """
    Расширенная админ-панель для управления пользователями
    Соответствует требованиям ТЗ 3.2.6, 3.2.10 и 5.4
    """
    
    list_display = ('username', 'email', 'role_display', 'is_active_status', 'date_joined', 'last_login')
    list_display_links = ('username',)
    list_filter = ('user_role__role', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    search_help_text = _('Поиск по имени пользователя, email, имени и фамилии')
    
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
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    ordering = ['-date_joined']
    list_per_page = 20
    inlines = [UserRoleInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_role')
    
    def role_display(self, obj):
        try:
            role = obj.user_role.role
            if role == 'admin':
                return format_html('<span style="color: #d9534f; font-weight: bold;">{}</span>', _('Администратор'))
            elif role == 'editor':
                return format_html('<span style="color: #5bc0de; font-weight: bold;">{}</span>', _('Редактор'))
            return '-'
        except UserRole.DoesNotExist:
            return '-'
    role_display.short_description = _('Роль')
    role_display.admin_order_field = 'user_role__role'
    
    def is_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ {}</span>', _('Активен'))
        return format_html('<span style="color: red; font-weight: bold;"> {}</span>', _('Неактивен'))
    is_active_status.short_description = _('Статус')
    is_active_status.admin_order_field = 'is_active'
    
    # Синхронизация прав ПОСЛЕ сохранения инлайна
    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        # Если сохраняется инлайн UserRole — применяем права немедленно
        if formset.model == UserRole:
            for form_obj in formset:
                if form_obj.instance.pk:
                    try:
                        form_obj.instance._sync_permissions()
                        if form_obj.changed_data:  # Если роль изменилась
                            messages.info(request, _('Права пользователя обновлены. Для применения разделов админки необходимо перезайти в систему.'))
                    except Exception as e:
                        messages.error(request, f'Ошибка синхронизации прав: {e}')

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
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'user_role'):
            UserRole.objects.create(user=obj)
        
        action = _("обновлен") if change else _("создан")
        print(f"Пользователь {obj.username} был {action} администратором {request.user.username}")

# Перерегистрация
admin.site.unregister(User)
admin.site.register(User, UserAdmin)