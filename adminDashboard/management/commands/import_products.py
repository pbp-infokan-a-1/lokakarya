import csv
import os
from django.core.management.base import BaseCommand
from adminDashboard.models import Product, Category, Store

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join('static', 'csv', 'product_dataset.csv')
        
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Assuming the CSV columns are: name, description, price, rating, num_reviews, category, store
                product, created = Product.objects.get_or_create(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    rating=row['rating'],
                    num_reviews=row['num_reviews']
                )
                
                # Handle categories
                categories = row['category'].split(',')
                for category_name in categories:
                    category, _ = Category.objects.get_or_create(name=category_name.strip())
                    product.category.add(category)
                
                # Handle stores
                stores = row['store'].split(',')
                for store_name in stores:
                    store, _ = Store.objects.get_or_create(name=store_name.strip())
                    product.stores.add(store)
                
                product.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported products from CSV'))