from django.apps import AppConfig
import os
from django.core.management import call_command


class StorepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storepage'  # Ganti dengan nama aplikasi Anda

    def ready(self):
        # Pastikan skrip hanya dijalankan dalam server yang aktif, bukan pada proses manajemen lain
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                # Panggil perintah loaddata untuk memuat fixture
                call_command('loaddata', 'store_data.json')  # Ganti dengan nama fixture Anda
                print("Data berhasil dimuat dari fixture.")
            except Exception as e:
                print(f"Gagal memuat data: {e}")