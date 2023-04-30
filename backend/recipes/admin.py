from django.contrib import admin
from .models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'name',
                    'cooking_time', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('color',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
