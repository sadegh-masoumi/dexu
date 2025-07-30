import re

import pandas as pd
from django.core.management.base import BaseCommand
from node.models import Node, Relation


class Command(BaseCommand):
    help = 'Import data from Dexu_challenge_samples.csv to Database'
    CHUNK_SIZE = 100

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading CSV: {e}"))
            return

        for _, row in df.iterrows():
            origin, created = Node.objects.get_or_create(name=row.username)

            found_usernames = set(re.findall(r'@(\w+)', row.data))

            for username in found_usernames:
                destination, created = Node.objects.get_or_create(name=username)
                relation = Relation.objects.filter(origin=origin, destination=destination).first()
                if relation:
                    relation.weight += 1
                    relation.save()
                else:
                    relation = Relation.objects.create(origin=origin, destination=destination, created_at=row.timestamp)

        self.stdout.write(self.style.SUCCESS('CSV import completed successfully.'))
