from django.contrib import admin
from django.contrib.admin import display

from .models import Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'name',
                    'cooking_time', 'created_at', 'added_in_favorites')
    readonly_fields = ('added_in_favorites',)
    search_fields = ('text',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('color',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
