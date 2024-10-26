from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Store, Category, Rating
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def adminDashboard(request):
    return render(request, 'adminDashboard.html')

import json

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('name')  # Order by 'name' or any other field
        paginator = Paginator(products, 16)  # Paginate the ordered queryset
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        product_list = [{
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'rating': product.rating.rating_value,
            'num_reviews': product.num_reviews,
            'categories': [category.name for category in product.category.all()],
            'stores': [store.name for store in product.stores.all()]  # Include related stores
        } for product in page_obj]
        
        response_data = {'products': product_list, 'page': page_obj.number, 'num_pages': paginator.num_pages}
        print(json.dumps(response_data, indent=4))  # Log the response data
        return JsonResponse(response_data)

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            rating_id = request.POST.get('rating')  # this might be empty or None

            print(name, description, price, rating_id)

            # Get rating based on ID if provided, otherwise set to 0
            if rating_id:
                rating = get_object_or_404(Rating, id=rating_id)
            else:
                # Either get the existing 0.0 rating or create it
                rating, created = Rating.objects.get_or_create(rating_value=0.0)

            # Create the new product with the default rating if needed
            new_product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                rating=rating
            )

            # Return a success response
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
