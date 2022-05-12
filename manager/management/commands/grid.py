import time

from django.core.management import BaseCommand

from manager.models import GridPosition


class Command(BaseCommand):

    ROWS = 10
    COLUMNS = 20

    @classmethod
    def _get_all_grid_positions(cls):
        for i in range(cls.ROWS):
            for j in range(cls.COLUMNS):
                yield GridPosition(x_position=i, y_position=j)

    def handle(self, *args, **options):
        GridPosition.objects.bulk_create(self._get_all_grid_positions())
