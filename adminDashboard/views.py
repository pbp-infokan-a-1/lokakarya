from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Store, Category, Rating
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def adminDashboard(request):
    return render(request, 'adminDashboard.html')

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_list = [{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'rating': product.rating.rating_value,
            'num_reviews': product.num_reviews,
            'categories': [category.name for category in product.category.all()]
        } for product in products]
        return JsonResponse({'products': product_list})

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        rating_id = request.POST.get('rating_id')
        category_ids = request.POST.getlist('category_ids')
        store_id = request.POST.get('store_id')
        
        rating = get_object_or_404(Rating, id=rating_id)
        store = get_object_or_404(Store, id=store_id)
        new_product = Product.objects.create(name=name, description=description, price=price, rating=rating, store=store)
        new_product.category.set(Category.objects.filter(id__in=category_ids))
        
        return JsonResponse({'status': 'success', 'product': {'id': new_product.id, 'name': new_product.name}})

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        rating_id = request.POST.get('rating_id')
        category_ids = request.POST.getlist('category_ids')
        
        product.rating = get_object_or_404(Rating, id=rating_id)
        product.category.set(Category.objects.filter(id__in=category_ids))
        product.save()

        return JsonResponse({'status': 'success', 'product': {'id': product.id, 'name': product.name}})

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def store_list(request):
    if request.method == 'GET':
        stores = Store.objects.all()
        store_list = [{
            'id': store.id,
            'name': store.name,
            'openDays': store.openDays,
            'address': store.address,
            'email': store.email,
            'phone': store.phone
        } for store in stores]
        return JsonResponse({'stores': store_list})

@csrf_exempt
def create_store(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        openDays = request.POST.get('openDays')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        new_store = Store.objects.create(name=name, openDays=openDays, address=address, email=email, phone=phone)
        return JsonResponse({'status': 'success', 'store': {'id': new_store.id, 'name': new_store.name}})

@csrf_exempt
def update_store(request, store_id):
    if request.method == 'POST':
        store = get_object_or_404(Store, id=store_id)
        store.name = request.POST.get('name')
        store.openDays = request.POST.get('openDays')
        store.address = request.POST.get('address')
        store.email = request.POST.get('email')
        store.phone = request.POST.get('phone')
        store.save()

        return JsonResponse({'status': 'success', 'store': {'id': store.id, 'name': store.name}})

@csrf_exempt
def delete_store(request, store_id):
    if request.method == 'POST':
        store = get_object_or_404(Store, id=store_id)
        store.delete()
        return JsonResponse({'status': 'success'})
