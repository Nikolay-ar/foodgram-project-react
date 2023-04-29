from django.contrib import admin

from .models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'author', 'name',
                    'cooking_time', 'created_at')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('created_at',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name', 'color', 'slug')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('name',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('color',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
