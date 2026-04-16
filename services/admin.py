from django.contrib import admin
from django.utils.html import format_html
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Административная панель для управления услугами
    """
    
    # 1. Просмотр списка всех услуг
    list_display = ('name', 'category', 'is_active_status', 'image_preview', 'created_at', 'updated_at')
    list_display_links = ('name',)
    
    # 6. Поиск по названию
    search_fields = ('name', 'description', 'short_description')
    search_help_text = 'Поиск по заголовку, описанию и краткому описанию'
    
    # 7. Фильтрация по категории и дате
    list_filter = ('category', 'is_active', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    # Поля формы редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'is_active'),
            'classes': ('wide',)
        }),
        ('Описание', {
            'fields': ('short_description', 'description'),
            'classes': ('wide',)
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('wide',)
        }),
        ('Служебная информация', {
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
    
    # Отображение статуса активности
    def is_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Активна</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Неактивна</span>')
    is_active_status.short_description = 'Статус'
    is_active_status.admin_order_field = 'is_active'
    
    # Предварительный просмотр изображения
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Нет изображения</span>')
    image_preview.short_description = 'Изображение'