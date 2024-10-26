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
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'rating': product.rating.rating_value,
            'num_reviews': product.num_reviews,
            'categories': [category.name for category in product.category.all()],
            'stores': [store.name for store in product.stores.all()]  # Include related stores
        } for product in products]
        return JsonResponse({'products': product_list})

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            rating_id = request.POST.get('rating')
            category_ids = request.POST.getlist('category')
            store_ids = request.POST.getlist('stores')  # List for multiple stores

            # Check required fields
            if not (name and price and rating_id):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            # Get related models
            rating = get_object_or_404(Rating, id=rating_id)

            # Create product
            new_product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                rating=rating,
            )

            # Set Many-to-Many relationships
            if category_ids:
                new_product.category.set(Category.objects.filter(id__in=category_ids))
            if store_ids:
                new_product.stores.set(Store.objects.filter(id__in=store_ids))

            return JsonResponse({'status': 'success', 'product': {'id': str(new_product.id), 'name': new_product.name}})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def update_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        rating_id = request.POST.get('rating')
        category_ids = request.POST.getlist('category')
        store_ids = request.POST.getlist('stores')

        product.rating = get_object_or_404(Rating, id=rating_id)

        # Update Many-to-Many relationships
        product.category.set(Category.objects.filter(id__in=category_ids))
        product.stores.set(Store.objects.filter(id__in=store_ids))
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
        stores = Store.objects.all()
        store_list = [{
            'id': store.id,
            'name': store.name,
            'openDays': store.openDays,
            'address': store.address,
            'email': store.email,
            'phone': store.phone,
            'products': [product.name for product in store.products.all()]  # Include related products
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
        product_ids = request.POST.getlist('products')  # List for multiple products

        if not name:
            return JsonResponse({'status': 'error', 'message': 'Store name is required'}, status=400)

        # Create store
        new_store = Store.objects.create(name=name, openDays=openDays, address=address, email=email, phone=phone)

        # Set Many-to-Many relationships
        if product_ids:
            new_store.products.set(Product.objects.filter(id__in=product_ids))

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
        product_ids = request.POST.getlist('products')

        store.save()

        # Update Many-to-Many relationships
        store.products.set(Product.objects.filter(id__in=product_ids))

        return JsonResponse({'status': 'success', 'store': {'id': store.id, 'name': store.name}})

@csrf_exempt
def delete_store(request, store_id):
    if request.method == 'POST':
        store = get_object_or_404(Store, id=store_id)
        store.delete()
        return JsonResponse({'status': 'success'})
