from django.contrib import admin
from django.utils.html import format_html
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """
    Административная панель для управления страницами
    Соответствует требованиям ТЗ 3.2.4
    """
    
    # 1. Список страниц с отображением slug, названия и даты последнего изменения
    list_display = ('title', 'slug_display', 'is_active_status', 'updated_at')
    list_display_links = ('title',)
    
    # Поиск по названию и содержимому
    search_fields = ('title', 'content', 'meta_title', 'meta_description')
    search_help_text = 'Поиск по названию, содержимому и SEO-полям'
    
    # Фильтрация по активности и дате
    list_filter = ('is_active', 'updated_at', 'created_at')
    date_hierarchy = 'updated_at'
    
    # Поля формы редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'is_active'),
            'classes': ('wide',)
        }),
        ('Текстовое содержимое', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('SEO-мета-данные', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Опциональные SEO-поля для улучшения индексации страницы поисковыми системами'
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
    
    # Отображение slug с подсказкой
    def slug_display(self, obj):
        return format_html(
            '<code>{}</code>',
            obj.slug
        )
    slug_display.short_description = 'Slug'
    slug_display.admin_order_field = 'slug'
    
    # Отображение статуса активности
    def is_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Активна</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Неактивна</span>')
    is_active_status.short_description = 'Статус'
    is_active_status.admin_order_field = 'is_active'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Инструкция внутри текстбокса для форматирования
        form.base_fields['content'].widget.attrs.update({
            'placeholder': 'Примеры HTML-разметки:\n<h1>Заголовок</h1>\n<p>Обычный текст</p>\n<b>жирный</b>\n<i>курсив</i>\n<ul><li>список</li></ul>\n<a href="#">ссылка</a>',
            'style': 'min-height: 400px !important; font-family: monospace; white-space: pre-wrap;'
        })
        
        # Подсказки для SEO-полей
        form.base_fields['meta_title'].widget.attrs.update({
            'placeholder': 'Рекомендуемая длина: до 60 символов',
            'style': 'max-width: 600px;'
        })
        
        form.base_fields['meta_description'].widget.attrs.update({
            'placeholder': 'Рекомендуемая длина: до 160 символов',
            'style': 'min-height: 80px !important; max-width: 600px;'
        })
        
        form.base_fields['meta_keywords'].widget.attrs.update({
            'placeholder': 'Ключевые слова через запятую',
            'style': 'max-width: 600px;'
        })
        
        return form