# Generated by Django 4.2.2 on 2023-06-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_cooking_time_alter_recipe_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/images/', verbose_name='Изображение рецепта'),
        ),
    ]
