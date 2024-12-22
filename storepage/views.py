import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from productpage.models import Product
from .models import Toko
from .forms import StoreForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

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

def show_all_json(request):
    toko_data = Toko.objects.all()
    toko_list = list(toko_data.values()) 
    return JsonResponse(toko_list, safe=False)

def store_products_json(request, store_id):
    store = get_object_or_404(Toko, id=store_id)
    products = store.get_products()  
    data = {
        'products': [
            {
                'id' : product.id,
                'name': product.name,  
                'min_price': str(product.min_price), 
                'max_price': str(product.max_price) 
            }
            for product in products
        ]
    }
    
    return JsonResponse(data)

def fetch_image(request, store_id):
    toko = get_object_or_404(Toko, id=store_id)
    if toko.image:
        image_name = os.path.basename(str(toko.image))
        image_path = os.path.join(settings.BASE_DIR, 'storepage', 'static', 'images', image_name)
        try:
            with open(image_path, 'rb') as img_file:
                return HttpResponse(img_file.read(), content_type='image/jpeg')
        except FileNotFoundError:
            return HttpResponse("Image file not found", status=404)
    else:
        return HttpResponse("No image assigned", status=404)

def fetch_product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.image:
        image_name = os.path.basename(str(product.image))
        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'products', image_name)       
        try:
            with open(image_path, 'rb') as img_file:
                return HttpResponse(img_file.read(), content_type='image/jpeg')
        except FileNotFoundError:
            return HttpResponse("Image file not found", status=404)
    else:
        return HttpResponse("No image assigned", status=404)
    
@csrf_exempt
def add_store_flutter(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=405)

    try:
        # Data akan ada di request.POST karena CookieRequest mengirim sebagai form-data
        # Debug: Print all POST data
        print("POST Data:", request.POST)
        
        # Validate required fields
        required_fields = ['nama', 'alamat', 'hari_buka', 'email', 'telepon']
        for field in required_fields:
            if not request.POST.get(field):
                print(f"Missing required field: {field}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }, status=400)

        # Create toko instance
        toko = Toko(
            nama=request.POST['nama'],
            alamat=request.POST['alamat'],
            hari_buka=request.POST['hari_buka'],
            email=request.POST['email'],
            telepon=request.POST['telepon'],
            gmaps_link=request.POST.get('gmaps_link', '')
        )

        toko.save()

        # Handle base64 image if present
        if 'image' in request.POST and request.POST['image']:
            try:
                # Decode base64 string
                base64_data = request.POST['image']
                # Remove data URL prefix if present
                if ',' in base64_data:
                    base64_data = base64_data.split(',')[1]
                
                image_data = base64.b64decode(base64_data)
                
                # Generate filename
                filename = f"store_{toko.id}_image.jpg"  # Default to jpg
                relative_path = os.path.join('images', filename).replace('\\', '/')
                full_path = os.path.join(settings.BASE_DIR, 'storepage', 'static', 'images', filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Save image file
                with open(full_path, 'wb') as f:
                    f.write(image_data)
                
                # Save path to model
                toko.image = relative_path
                toko.save()

            except Exception as e:
                print("Error saving image:", str(e))
                if toko.id:
                    toko.delete()
                raise Exception(f"Failed to save image: {str(e)}")

        return JsonResponse({
            "status": "success",
            "message": "Store created successfully",
            "store_id": toko.id
        }, status=201)

    except Exception as e:
        print(f"Error in add_store_flutter: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": f"Failed to create store: {str(e)}"
        }, status=500)

@csrf_exempt
def edit_store_flutter(request, store_id):
    if request.method == 'POST':
        try:
            toko = get_object_or_404(Toko, id=store_id)

            # Mengambil data dari POST
            nama = request.POST.get('nama', toko.nama)
            alamat = request.POST.get('alamat', toko.alamat)
            hari_buka = request.POST.get('hari_buka', toko.hari_buka)
            email = request.POST.get('email', toko.email)
            telepon = request.POST.get('telepon', toko.telepon)
            gmaps_link = request.POST.get('gmaps_link', toko.gmaps_link)

            # Handle base64 image if present
            if 'image' in request.POST and request.POST['image']:
                try:
                    # Menghapus gambar lama jika ada
                    if toko.image:
                        old_image_path = os.path.join(settings.BASE_DIR, 'storepage', 'static', str(toko.image))
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    
                    # Decode base64 string
                    base64_data = request.POST['image']
                    # Remove data URL prefix if present
                    if ',' in base64_data:
                        base64_data = base64_data.split(',')[1]
                    
                    image_data = base64.b64decode(base64_data)
                    
                    # Generate filename
                    filename = f"store_{store_id}_image.jpg"  # Default to jpg
                    relative_path = os.path.join('images', filename).replace('\\', '/')
                    full_path = os.path.join(settings.BASE_DIR, 'storepage', 'static', 'images', filename)
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    # Save image file
                    with open(full_path, 'wb') as f:
                        f.write(image_data)
                    
                    # Save path to model
                    toko.image = relative_path

                except Exception as e:
                    print("Error saving image:", str(e))
                    return JsonResponse({
                        "status": "error",
                        "message": f"Failed to save image: {str(e)}"
                    }, status=500)

            # Update fields
            toko.nama = nama
            toko.alamat = alamat
            toko.hari_buka = hari_buka
            toko.email = email
            toko.telepon = telepon
            toko.gmaps_link = gmaps_link

            toko.save()

            return JsonResponse({
                "status": "success", 
                "message": "Store updated successfully"
            }, status=200)

        except Toko.DoesNotExist:
            return JsonResponse({
                "status": "error", 
                "message": "Store not found"
            }, status=404)
        except Exception as e:
            print("Error in edit_store_flutter:", str(e))  # Tambahkan logging
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=405)

@csrf_exempt
def delete_store_flutter(request, store_id):
    if request.method == 'GET':
        try:
            toko = get_object_or_404(Toko, id=store_id)

            # Menghapus gambar jika ada
            if toko.image:
                image_path = os.path.join(settings.BASE_DIR, toko.image.name)
                if os.path.exists(image_path):
                    os.remove(image_path)

            toko.delete()

            return JsonResponse({"status": "success", "message": "Store deleted successfully"}, status=200)

        except Toko.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Store not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
