from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import TokoForm, ProductForm
from storepage.models import Toko
from productpage.models import Product
from django.views.decorators.http import require_http_methods
import uuid

@login_required
def adminDashboard(request):
    # Pass initial data to template if needed (for non-AJAX loading)
    stores = Toko.objects.all()
    products = Product.objects.all()
    return render(request, 'adminDashboard.html', {'stores': stores, 'products': products})

@login_required
@require_http_methods(["GET", "POST"])
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'product': {
                        'id': str(product.id),
                        'name': product.name,
                        'description': product.description,
                        'min_price': product.min_price,
                        'max_price': product.max_price,
                        'categories': [cat.name for cat in product.category.all()],
                        'stores': [store.nama for store in product.store.all()]
                    }
                })
            return redirect('adminDashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            return render(request, 'adminDashboard/add_product.html', {'form': form})
    else:
        form = ProductForm()
    return render(request, 'adminDashboard/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    # Convert string UUID to UUID object
    product_uuid = uuid.UUID(product_id)
    product = get_object_or_404(Product, id=product_uuid)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('adminDashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminDashboard/edit_product.html', {'form': form})

@login_required
def delete_product(request, product_id):
    # Convert string UUID to UUID object
    product_uuid = uuid.UUID(product_id)
    product = get_object_or_404(Product, id=product_uuid)
    if request.method == 'POST':
        product.delete()
        return redirect('adminDashboard')
    return render(request, 'adminDashboard/delete_product.html', {'product': product})

@login_required
def add_store(request):
    if request.method == 'POST':
        form = TokoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminDashboard')  # Redirect to dashboard after adding store
    else:
        form = TokoForm()
    return render(request, 'adminDashboard/add_store.html', {'form': form})

@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Toko, id=store_id)
    if request.method == 'POST':
        form = TokoForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('adminDashboard')  # Redirect to dashboard after editing store
    else:
        form = TokoForm(instance=store)
    return render(request, 'adminDashboard/edit_store.html', {'form': form})

@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Toko, id=store_id)
    if request.method == 'POST':
        store.delete()
        return redirect('adminDashboard')  # Redirect to dashboard after deleting store
    return render(request, 'adminDashboard/delete_store.html', {'store': store})

# AJAX View to return list of stores
@login_required
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_data = [{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'categories': [category.name for category in product.category.all()],
            'stores': [store.name for store in product.stores.all()]
        } for product in products]
        return JsonResponse({'products': product_data})

@login_required
def store_list(request):
    if request.method == 'GET':
        stores = Toko.objects.all()
        store_data = [{
            'id': store.id,
            'name': store.name,
            'open_days': store.openDays,
            'address': store.address,
            'email': store.email,
            'phone': store.phone,
            'products': [product.name for product in store.product.all()]
        } for store in stores]
        return JsonResponse({'stores': store_data})