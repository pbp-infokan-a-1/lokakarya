from django.apps import AppConfig
import os
from django.core.management import call_command

class ProductpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productpage'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                call_command('loaddata', 'categories.json')
                call_command('loaddata', 'product_data.json')
                print("Data produk berhasil dimuat.")
            except Exception as e:
                print(f"Gagal memuat data: {e}")