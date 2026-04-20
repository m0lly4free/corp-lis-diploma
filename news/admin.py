from django.contrib import admin
from django.utils.html import format_html
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Административная панель для новостей с инструкцией внутри текстбокса
    """
    
    # 1. Просмотр списка всех новостей
    list_display = ('title', 'is_active_status', 'image_preview', 'created_at', 'updated_at')
    list_display_links = ('title',)
    
    # 5. Поиск по заголовку
    search_fields = ('title', 'content', 'short_description')
    search_help_text = 'Поиск по заголовку, содержанию и краткому описанию'
    
    # 6. Фильтрация по дате публикации
    list_filter = ('is_active', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    # Поля формы редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'is_active'),
            'classes': ('wide',)
        }),
        ('Описание', {
            'fields': ('short_description', 'content'),
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
    save_as = True
    
    # Автоматическое заполнение slug
    prepopulated_fields = {'slug': ('title',)}
    
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
    image_preview.short_description = 'Миниатюра'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # ИНСТРУКЦИЯ ВНУТРИ ТЕКСТБОКСА КАК PLACEHOLDER
        form.base_fields['short_description'].widget.attrs.update({
            'placeholder': 'Примеры HTML-разметки:\n<b>жирный</b>\n<i>курсив</i>\n<u>подчеркнутый</u>\n<h2>заголовок 2</h2>\n<ul><li>список</li></ul>',
            'style': 'min-height: 150px !important; font-family: monospace; white-space: pre-wrap;'
        })
        
        form.base_fields['content'].widget.attrs.update({
            'placeholder': 'Примеры HTML-разметки:\n<b>жирный</b>\n<i>курсив</i>\n<u>подчеркнутый</u>\n<h2>заголовок 2</h2>\n<ul><li>список</li></ul>',
            'style': 'min-height: 300px !important; font-family: monospace; white-space: pre-wrap;'
        })
        
        return form