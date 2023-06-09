# Generated by Django 3.2 on 2023-05-11 15:23

import csv
from django.db import migrations


with open('ingredients.csv', 'r', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    headers = dr.fieldnames
    INITIAL_INGREDIENTS = [{headers[0]: i['name'], headers[1]: i['measurement_unit']} for i in dr]


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model("recipes", "Ingredient")
    for ingredient in INITIAL_INGREDIENTS:
        new_ingredient = Ingredient(**ingredient)
        new_ingredient.save()


def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model("recipes", "Ingredient")
    for ingredient in INITIAL_INGREDIENTS:
        Ingredient.objects.get(slug=ingredient['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_add_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        )
    ]
