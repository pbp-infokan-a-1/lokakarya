import json
from uuid import UUID
from django.core.management.base import BaseCommand
from productpage.models import Product, Category
from storepage.models import Toko

class Command(BaseCommand):
    help = 'Load product data from a JSON file'

    def handle(self, *args, **kwargs):
        # Load product data
        with open('productpage/fixtures/product_data.json', 'r') as file:
            data = json.load(file)

        for item in data:
            if item['model'] == 'productpage.product':
                product_name = item['fields']['name']
                category_id = item['fields']['category']
                min_price = item['fields']['min_price']
                max_price = item['fields']['max_price']
                description = item['fields']['description']
                store_ids = item['fields'].get('store', [])

                # Fetch existing products by name
                products = Product.objects.filter(name=product_name)
                
                if products.exists():
                    # Handle multiple products with the same name
                    if products.count() > 1:
                        self.stdout.write(self.style.ERROR(f"Multiple products found with name '{product_name}'. Skipping..."))
                        continue  # Skip to the next item

                    # Get the first product (assumed to be the correct one)
                    product = products.first()
                else:
                    # Create a new product instance
                    product = Product(
                        name=product_name,
                        category_id=category_id,
                        min_price=min_price,
                        max_price=max_price,
                        description=description,
                    )
                    product.save()  # Save the new product

                # Set the Many-to-Many relationship for stores
                stores = Toko.objects.filter(id__in=store_ids)  # Fetch Toko instances based on IDs
                product.store.set(stores)  # Associate the stores with the product
                product.save()  # Save the product instance

                self.stdout.write(self.style.SUCCESS(f"Processed product: {product_name}"))
