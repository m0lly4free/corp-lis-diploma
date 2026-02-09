# core/models.py

from django.db import models

class Page(models.Model):
    slug = models.SlugField("URL-путь", max_length=100, unique=True)
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержимое")
    meta_title = models.CharField("SEO заголовок", max_length=255, blank=True)
    meta_description = models.TextField("SEO описание", blank=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.title