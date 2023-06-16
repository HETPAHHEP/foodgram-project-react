import os
from csv import reader as read_csv

from django.core.management import BaseCommand, CommandError
from django.db.transaction import atomic
from recipes.models import Ingredient

from foodgram.settings import BASE_DIR


class Command(BaseCommand):
    """
    Команда Django для импорта ингредиентов из CSV
    в соответствующую таблицу
    """
    help = 'Loads Ingredients data from CSV'

    @atomic
    def handle(self, *args, **options):
        csv_file = 'ingredients.csv'
        path_to_csv = os.path.join(BASE_DIR, 'recipes/init_data', csv_file)

        with open(path_to_csv, 'r', encoding='utf-8') as file:
            reader = read_csv(file)
            total_rows = 0

            for i, row in enumerate(reader):
                try:
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
                    total_rows = i

                except ValueError as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error report problem:\n\n'
                        f'ID ROW: {i}\n\n'
                        f'ROW: {row}\n\n'
                        f'Error details: {str(e)}'
                    ))
                    raise CommandError('Error while adding data')

        self.stdout.write(self.style.SUCCESS(
            f'{Ingredient.__name__} data from {csv_file} '
            f'imported successfully. '
            f'Total rows: {total_rows}'
        ))
