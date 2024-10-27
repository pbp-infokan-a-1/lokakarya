from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Toko
from .forms import StoreForm

# Menampilkan daftar toko
def toko_list(request):
    toko_list = Toko.objects.all()
    return render(request, 'storepage.html', {'toko_list': toko_list})

def storedetail(request, store_id):
    # Mengambil toko berdasarkan ID
    store = get_object_or_404(Toko, id=store_id)
    
    # Mengambil semua produk yang terkait dengan toko ini
    products = store.get_products()  # Menggunakan metode get_products

    context = {
        'store': store,
        'products': products,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'storedetail.html', context)

def store_api_create(request):
    if request.method == 'POST':
        try:
            form = StoreForm(request.POST, request.FILES)
            if form.is_valid():
                store = form.save()
                return JsonResponse({'message': 'Store created successfully'})
            return JsonResponse({'message': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

def store_api_update(request, pk):
    try:
        store = Toko.objects.get(pk=pk)
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Store updated successfully'})
        return JsonResponse({'message': form.errors}, status=400)
    except Toko.DoesNotExist:
        return JsonResponse({'message': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def store_api_delete(request, pk):
    try:
        store = Toko.objects.get(pk=pk)
        store.delete()
        return JsonResponse({'message': 'Store deleted successfully'})
    except Toko.DoesNotExist:
        return JsonResponse({'message': 'Store not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def store_api_get(request, pk):
    try:
        store = Toko.objects.get(pk=pk)
        data = {
            'nama': store.nama,
            'alamat': store.alamat,
            'hari_buka': store.hari_buka,
            'email': store.email,
            'telepon': store.telepon,
            'image_url': store.image.url if store.image else None
        }
        return JsonResponse(data)
    except Toko.DoesNotExist:
        return JsonResponse({'message': 'Store not found'}, status=404)

def is_admin(user):
    return user.groups.filter(role='Admin').exists()
