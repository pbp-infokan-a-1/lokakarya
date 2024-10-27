import os
import csv
from django.core.management.base import BaseCommand
from adminDashboard.models import Product, Category, Toko

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join('static', 'csv', 'product_dataset.csv')
        
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category, _ = Category.objects.get_or_create(name=row['Category'].strip())
                
                product, created = Product.objects.get_or_create(
                    name=row['Name'].strip(),
                    category=category,
                    min_price=row['MinPrice'],
                    max_price=row['MaxPrice'],
                    description=row['Description'].strip()
                )
                
                # Handle stores
                store_names = row['Store'].split(',')
                for store_name in store_names:
                    store_name = store_name.strip()
                    store, _ = Toko.objects.get_or_create(name=store_name)
                    product.stores.add(store)
                
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {product.name}'))