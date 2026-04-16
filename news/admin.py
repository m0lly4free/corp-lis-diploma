from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админ-панель для управления новостями"""
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    # Настройка формы
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'content', 'image'),
        }),
        ('Дата и статус', {
            'fields': ('created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',),
        }),
    )
    
    # Только чтение для дат
    readonly_fields = ('created_at', 'updated_at')
    
    # Порядок полей в форме
    ordering = ('-created_at',)
    
    # Параметры для фильтрации
    list_editable = ('is_active',)
    
    # Поля для поиска
    search_help_text = "Можно искать по заголовку, содержанию и краткому описанию"
    
    # Настройка отображения
    save_on_top = True
    save_as = True