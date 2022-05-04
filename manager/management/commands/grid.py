from django.core.management import BaseCommand

from manager.models import GridPosition

ROWS = 10
COLUMNS = 20


class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(ROWS):
            for j in range(COLUMNS):
                GridPosition(x_position=i, y_position=j).save()
