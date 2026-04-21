from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Административная панель для управления услугами
    Соответствует требованиям ТЗ 3.2.6 и 3.2.10
    """
    
    # 1. Просмотр списка всех услуг
    list_display = ('name', 'category_display', 'is_active_status', 'image_preview', 'created_at', 'updated_at')
    list_display_links = ('name',)
    
    # 6. Поиск по названию
    search_fields = ('name', 'description', 'short_description')
    search_help_text = _('Поиск по заголовку, описанию и краткому описанию')
    
    # 7. Фильтрация по категории и дате
    list_filter = ('category', 'is_active', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    # Поля формы редактирования
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'slug', 'category', 'is_active'),
            'classes': ('wide',)
        }),
        (_('Описание'), {
            'fields': ('short_description', 'description'),
            'classes': ('wide',)
        }),
        (_('Изображение'), {
            'fields': ('image',),
            'classes': ('wide',)
        }),
        (_('Служебная информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    # Только для чтения служебные поля
    readonly_fields = ('created_at', 'updated_at')
    
    # Параметры отображения
    list_per_page = 20
    save_on_top = True
    
    # Автоматическое заполнение slug
    prepopulated_fields = {'slug': ('name',)}
    
    def get_queryset(self, request):
        # Оптимизация запросов к базе данных
        return super().get_queryset(request)
    
    # Отображение категории с переводом
    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = _('Категория')
    category_display.admin_order_field = 'category'
    
    # Отображение статуса активности
    def is_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ {}</span>', _('Активна'))
        return format_html('<span style="color: red; font-weight: bold;">✗ {}</span>', _('Неактивна'))
    is_active_status.short_description = _('Статус')
    is_active_status.admin_order_field = 'is_active'
    
    # Предварительный просмотр изображения
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">{}</span>', _('Нет изображения'))
    image_preview.short_description = _('Изображение')
    
    # Обработка конфликтов при одновременном редактировании
    def response_change(self, request, obj):
        original_version = request.POST.get('original_version')
        if original_version and int(original_version) != obj.version - 1:
            messages.warning(
                request, 
                _('Данные услуги были изменены другим редактором. '
                  'Пожалуйста, обновите страницу и внесите изменения снова.')
            )
            return HttpResponseRedirect(reverse('admin:services_service_change', args=[obj.id]))
        return super().response_change(request, obj)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            extra_context['original_version'] = obj.version if obj else 0
        return super().change_view(request, object_id, form_url, extra_context)