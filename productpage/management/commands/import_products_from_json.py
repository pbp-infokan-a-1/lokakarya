# productpage/management/commands/import_products_from_json.py
import json
from django.core.management.base import BaseCommand
from productpage.models import Product
from storepage.models import Toko
import random

class Command(BaseCommand):
    help = 'Import products from a JSON file and associate them with stores'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing product data')

    def handle(self, *args, **options):
        json_file = options['json_file']

        # Load data from JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if 'fields' in item:
                print(item['fields'])
                fields = item['fields']
                product = Product(
                    name=fields["name"],
                    min_price= random.randint(0, 5) * 1000,
                    max_price= random.randint(0, 5) * 1000,
                    description= "Ini Product",
                )
                product.save()
            else:
                self.stdout.write(self.style.WARNING(f'Missing fields in item: {item}'))


            self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
