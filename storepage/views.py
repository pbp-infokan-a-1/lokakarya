from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Toko
from django.views.decorators.http import require_http_methods
from .models import Toko
import json


# Menampilkan daftar toko
def toko_list(request):
    toko_list = Toko.objects.all()
    return render(request, 'storepage.html', {'toko_list': toko_list})


# API untuk mendapatkan data toko tertentu
@require_http_methods(["GET"])
def get_store(request, store_id):
    store = get_object_or_404(Toko, id=store_id)
    data = {
        "nama": store.nama,
        "alamat": store.alamat,
        "hari_buka": store.hari_buka,
        "email": store.email,
        "telepon": store.telepon,
        "gmaps_link": store.gmaps_link,
    }
    return JsonResponse(data)


# API untuk membuat toko baru
@require_http_methods(["POST"])
def create_store(request):
    try:
        data = json.loads(request.body)
        new_store = Toko.objects.create(
            nama=data['nama'],
            alamat=data['alamat'],
            hari_buka=data['hari_buka'],
            email=data['email'],
            telepon=data['telepon'],
            gmaps_link=data.get('gmaps_link', ''),
        )
        return JsonResponse({'status': 'success', 'id': new_store.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# API untuk mengupdate data toko
@require_http_methods(["POST"])
def update_store(request, store_id):
    try:
        data = json.loads(request.body)
        store = get_object_or_404(Toko, id=store_id)
        store.nama = data['nama']
        store.alamat = data['alamat']
        store.hari_buka = data['hari_buka']
        store.email = data['email']
        store.telepon = data['telepon']
        store.gmaps_link = data.get('gmaps_link', '')
        store.save()
        return JsonResponse({'status': 'success'})
    except Toko.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# API untuk menghapus data toko
@require_http_methods(["POST"])
def delete_store(request, store_id):
    try:
        store = get_object_or_404(Toko, id=store_id)
        store.delete()
        return JsonResponse({'status': 'success'})
    except Toko.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Store not found'}, status=404)

def storedetail(request, store_id):
    store = get_object_or_404(Toko, id=store_id)
    return render(request, 'storedetail.html', {'store': store})