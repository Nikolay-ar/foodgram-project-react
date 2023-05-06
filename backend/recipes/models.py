from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Наименование ингредиента')
    measurement_unit = models.CharField(max_length=100,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.TextField(max_length=200, verbose_name='Название тэга',
                            unique=True)
    color = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(unique=True, max_length=200,
                            verbose_name='Уникальный слаг')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта',
                               db_index=True)
    text = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1, message='Мин значение 1!')])
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Тэги рецепта',
                                  blank=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата публикации',
                                      db_index=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент есть в рецептах')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Ингредиенты рецепта')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, message='Мин количество 1!')])

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
