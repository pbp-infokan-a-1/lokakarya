import threading
from django.core.management import call_command

class LoadDataMiddleware:
    _data_loaded = False
    _lock = threading.Lock()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with self._lock:
            if not self._data_loaded:
                try:
                    call_command('loaddata', 'store_data.json')  # Ganti dengan nama fixture Anda
                    self._data_loaded = True
                    print("Data berhasil dimuat dari fixture.")
                except Exception as e:
                    print(f"Gagal memuat data: {e}")
        response = self.get_response(request)
        return response
