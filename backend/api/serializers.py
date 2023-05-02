import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Subscribe, User


class TagSerializer(serializers.ModelSerializer):
    recipes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug', 'recipes']


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  "is_subscribed"
                  )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientCreateInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipeingredient_set')
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'created_at',
                  )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientCreateInRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer(read_only=True)

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Добавьте хотя бы один ингредиент.")
        return value

    def create(self, validated_data):
        """Если нам надо записывать в поле ingredients переопределяем метод
        create. Сохраняет в т.ч. данные из поля ingredients и tags"""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        create_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(
            create_ingredients
        )

        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        image = validated_data.pop('image', None)
        if ingredients is not None:
            instance.ingredients.clear()

            create_ingredients = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            RecipeIngredient.objects.bulk_create(
                create_ingredients
            )
        if tags is not None:
            instance.tags.clear()
            instance.tags.set(tags)
        if image is not None:
            instance.image.clear()
            instance.image.add(image)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time'
                  )


class RecipeShortSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
