from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe

User = get_user_model()


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(FilterSet):
    tags = CharFilterInFilter(field_name='tags__slug', lookup_expr='in')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset
