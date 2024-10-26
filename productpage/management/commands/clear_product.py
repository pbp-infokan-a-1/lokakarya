from django.core.management.base import BaseCommand
from productpage.models import Product

class Command(BaseCommand):
    help = 'Clear all records from the Product table'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared the Product table'))