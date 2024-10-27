from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Toko, Category, Rating
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

def adminDashboard(request):
    products = Product.objects.all()
    stores = Toko.objects.all()
    return render(request, 'adminDashboard.html', {'products': products, 'stores': stores})

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('name')
        paginator = Paginator(products, 16)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        product_list = [{
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'min_price': str(product.min_price),
            'max_price': str(product.max_price),
            'average_rating': product.count_average_rating(),
            'num_reviews': product.num_reviews(),
            'category': product.category.name,
            'stores': [store.nama for store in product.store.all()]
        } for product in page_obj]
        
        response_data = {'products': product_list, 'page': page_obj.number, 'num_pages': paginator.num_pages}
        print(json.dumps(response_data, indent=4))
        return JsonResponse(response_data)

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            min_price = request.POST.get('min_price')
            max_price = request.POST.get('max_price')
            category_id = request.POST.get('category')
            store_ids = request.POST.getlist('stores')

            category = get_object_or_404(Category, id=category_id)
            new_product = Product.objects.create(
                name=name,
                description=description,
                min_price=min_price,
                max_price=max_price,
                category=category
            )

            if store_ids:
                new_product.store.set(Toko.objects.filter(id__in=store_ids))

            return JsonResponse({
                'status': 'success',
                'product': {'id': new_product.id, 'name': new_product.name}
            })
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.min_price = request.POST.get('min_price')
        product.max_price = request.POST.get('max_price')
        category_id = request.POST.get('category')
        store_ids = request.POST.getlist('stores')

        product.category = get_object_or_404(Category, id=category_id)
        product.store.set(Toko.objects.filter(id__in=store_ids))
        product.save()

        return JsonResponse({'status': 'success', 'product': {'id': str(product.id), 'name': product.name}})

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def store_list(request):
    if request.method == 'GET':
        stores = Toko.objects.all()
        store_list = [{
            'id': store.id,
            'name': store.nama,
            'openDays': store.hari_buka,
            'address': store.alamat,
            'email': store.email,
            'phone': store.telepon,
            'products': [product.name for product in store.products.all()]
        } for store in stores]
        return JsonResponse({'stores': store_list})

@csrf_exempt
def create_store(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        hari_buka = request.POST.get('hari_buka')
        alamat = request.POST.get('alamat')
        email = request.POST.get('email')
        telepon = request.POST.get('telepon')
        product_ids = request.POST.getlist('products')

        if not nama:
            return JsonResponse({'status': 'error', 'message': 'Store name is required'}, status=400)

        new_store = Toko.objects.create(nama=nama, hari_buka=hari_buka, alamat=alamat, email=email, telepon=telepon)

        if product_ids:
            new_store.products.set(Product.objects.filter(id__in=product_ids))

        return JsonResponse({'status': 'success', 'store': {'id': new_store.id, 'name': new_store.nama}})

@csrf_exempt
def update_store(request, store_id):
    if request.method == 'POST':
        store = get_object_or_404(Toko, id=store_id)
        store.nama = request.POST.get('nama')
        store.hari_buka = request.POST.get('hari_buka')
        store.alamat = request.POST.get('alamat')
        store.email = request.POST.get('email')
        store.telepon = request.POST.get('telepon')
        product_ids = request.POST.getlist('products')

        store.save()

        store.products.set(Product.objects.filter(id__in=product_ids))

        return JsonResponse({'status': 'success', 'store': {'id': store.id, 'name': store.nama}})

@csrf_exempt
def delete_store(request, store_id):
    if request.method == 'POST':
        store = get_object_or_404(Toko, id=store_id)
        store.delete()
        return JsonResponse({'status': 'success'})
