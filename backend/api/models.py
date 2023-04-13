from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Наименование ингредиента')
    measurment_unit = models.CharField(max_length=100,
                                       verbose_name='Единица измерения')

    def __str__(self):
        return f'({self.name} {self.measurment_unit})'


class Recipe(models.Model):
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe',
                                         verbose_name='Ингредиенты')
    tags = models.TextField()
    image = models.ImageField(upload_to='recipes/', null=True,
                              blank=True, verbose_name='Изображение')
    name = models.TextField(max_length=200, verbose_name='Название рецепта')
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    is_favorited = models.BooleanField(verbose_name='Есть в избранном')
    is_in_shopping_card = models.BooleanField(verbose_name='Есть в карзине')

    def __str__(self):
        return f'{self.name}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
