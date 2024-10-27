# productpage/management/commands/import_products_from_json.py
import json
from django.core.management.base import BaseCommand
from productpage.models import Product
from storepage.models import Toko

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
                fields = item['fields']
                product = Product(
                    name=fields["name"],
                    category=fields["category"],
                    min_price=fields["min_price"],
                    max_price=fields["max_price"],
                    description=fields["description"],
                    store=fields["store"]  # Ensure this key exists too
                )
                product.save()
            else:
                self.stdout.write(self.style.WARNING(f'Missing fields in item: {item}'))


            self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
