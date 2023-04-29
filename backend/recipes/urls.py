from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RecipesViewSet, IngredientViewSet, TagViewSet

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
]
