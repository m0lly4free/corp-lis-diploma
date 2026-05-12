from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Административная панель для управления обращениями
    Соответствует требованиям ТЗ 3.2.10
    """
    
    # 1. Просмотр всех входящих сообщений
    list_display = ('name', 'email', 'phone_display', 'is_processed_status', 'created_at')
    list_display_links = ('name',)
    
    # 4. Сортировка по дате
    ordering = ['-created_at']
    
    # 5. Фильтрация по статусу обработки
    list_filter = ('is_processed', 'created_at')
    date_hierarchy = 'created_at'
    
    # Поиск по основным полям
    search_fields = ('name', 'email', 'phone', 'message')
    search_help_text = _('Поиск по имени, email, телефону и тексту обращения')
    
    # Поля формы просмотра деталей
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'email', 'phone'),
            'classes': ('wide',)
        }),
        (_('Содержание обращения'), {
            'fields': ('message',),
            'classes': ('wide',)
        }),
        (_('Статус и служебная информация'), {
            'fields': ('is_processed', 'created_at', 'updated_at'),
            'classes': ('wide',)
        }),
    )
    
    # Только для чтения служебные поля
    readonly_fields = ('created_at', 'updated_at', 'name', 'email', 'phone', 'message')
    
    # Параметры отображения
    list_per_page = 20
    
    # Действия администратора
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    # 3. Отображение статуса в списке
    def is_processed_status(self, obj):
        if obj.is_processed:
            return format_html('<span style="color: green; font-weight: bold;">✅ {}</span>', _('Обработано'))
        return format_html('<span style="color: orange; font-weight: bold;">⏳ {}</span>', _('Новое'))
    is_processed_status.short_description = _('Статус')
    is_processed_status.admin_order_field = 'is_processed'
    
    # Отображение телефона (скрытие если пусто)
    def phone_display(self, obj):
        return obj.phone if obj.phone else '-'
    phone_display.short_description = _('Телефон')
    
    # 2. Просмотр детали обращения на отдельной странице
    def has_add_permission(self, request):
        """Запрет добавления обращений через админку"""
        return False
    
    # Действия для массовой обработки
    def mark_as_processed(self, request, queryset):
        """Пометить выбранные обращения как обработанные"""
        updated = queryset.update(is_processed=True)
        self.message_user(request, _('%(count)s обращений помечено как обработанные.') % {'count': updated})
    mark_as_processed.short_description = _('Пометить как обработанные')
    
    def mark_as_unprocessed(self, request, queryset):
        """Пометить выбранные обращения как необработанные"""
        updated = queryset.update(is_processed=False)
        self.message_user(request, _('%(count)s обращений помечено как необработанные.') % {'count': updated})
    mark_as_unprocessed.short_description = _('Пометить как необработанные')
    
    # Обработка конфликтов при одновременном редактировании
    def response_change(self, request, obj):
        original_version = request.POST.get('original_version')
        if original_version and int(original_version) != obj.version - 1:
            messages.warning(
                request, 
                _('Данные обращения были изменены другим администратором. '
                  'Пожалуйста, обновите страницу.')
            )
            return HttpResponseRedirect(reverse('admin:contacts_contactmessage_change', args=[obj.id]))
        return super().response_change(request, obj)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            extra_context['original_version'] = obj.version if obj else 0
        return super().change_view(request, object_id, form_url, extra_context)