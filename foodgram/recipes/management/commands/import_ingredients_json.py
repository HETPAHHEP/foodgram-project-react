import json
import os

from django.core.management import BaseCommand, CommandError
from django.db.transaction import atomic
from recipes.models import Ingredient

from foodgram.settings import BASE_DIR


class Command(BaseCommand):
    """
    Команда Django для импорта ингредиентов из JSON
    в соответствующую таблицу
    """
    help = 'Loads Ingredients data from JSON'

    @atomic
    def handle(self, *args, **options):
        json_file = 'ingredients.json'
        path_to_json = os.path.join(BASE_DIR, 'recipes/init_data', json_file)

        with open(path_to_json, 'r', encoding='utf-8') as file:
            reader = json.load(file)
            total_rows = len(reader)

            for i, row in enumerate(reader):
                try:
                    name = row['name']
                    measurement_unit = row['measurement_unit']

                    Ingredient.objects.create(
                        name=name,
                        measurement_unit=measurement_unit
                    )

                except ValueError as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error while adding data:\n\n'
                        f'ID ROW: {i}\n\n'
                        f'ROW: {row}\n\n'
                        f'Error details: {str(e)}'
                    ))
                    raise CommandError('Error while adding data')

        self.stdout.write(self.style.SUCCESS(
            f'{Ingredient.__name__} data from {json_file} '
            f'imported successfully. '
            f'Total rows: {total_rows}'))
