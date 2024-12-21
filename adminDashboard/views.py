from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .forms import TokoForm, ProductForm
from storepage.models import Toko
from productpage.models import Product, Category

@staff_member_required
def adminDashboard(request):
    stores = Toko.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'stores': stores,
        'products': products,
        'categories': categories,
        'store_form': TokoForm(),
        'product_form': ProductForm()
    }
    return render(request, 'adminDashboard.html', context)

@login_required
@require_http_methods(["GET"])
def product_list(request):
    products = Product.objects.all()
    products_data = [{
        'id': str(product.id),
        'name': product.name,
        'description': product.description,
        'min_price': str(product.min_price),
        'max_price': str(product.max_price),
        'category': [category.name for category in product.category.all()],
        'stores': [store.nama for store in product.store.all()],
        'image_url': product.image.url if product.image else None
    } for product in products]
    return JsonResponse({'success': True, 'products': products_data})

@login_required
@require_http_methods(["POST"])
def add_product(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save(commit=False)
        product.save()
        form.save_m2m()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_http_methods(["GET", "POST"])
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    # GET request - return product data for form population
    return JsonResponse({
        'success': True,
        'product': {
            'id': str(product.id),
            'name': product.name,
            'min_price': str(product.min_price),
            'max_price': str(product.max_price),
            'description': product.description,
            'category': [category.id for category in product.category.all()],
            'stores': [store.id for store in product.store.all()],
            'image_url': product.image.url if product.image else None
        }
    })

def delete_product(_, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["GET"])
def store_list(request):
    stores = Toko.objects.all()
    stores_data = [{
        'id': store.id,
        'nama': store.nama,
        'hari_buka': store.hari_buka,
        'alamat': store.alamat,
        'email': store.email,
        'telepon': store.telepon,
        'gmaps_link': store.gmaps_link,
        'image_url': store.image.url if store.image else None
    } for store in stores]
    return JsonResponse({'success': True, 'stores': stores_data})

@login_required
@require_http_methods(["POST"])
def add_store(request):
    form = TokoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_http_methods(["GET", "POST"])
def edit_store(request, store_id):
    store = get_object_or_404(Toko, id=store_id)
    if request.method == 'POST':
        form = TokoForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    # GET request - return store data for form population
    return JsonResponse({
        'success': True,
        'store': {
            'id': store.id,
            'nama': store.nama,
            'hari_buka': store.hari_buka,
            'alamat': store.alamat,
            'email': store.email,
            'telepon': store.telepon,
            'gmaps_link': store.gmaps_link,
            'image_url': store.image.url if store.image else None
        }
    })

def delete_store(_, store_id):
    store = get_object_or_404(Toko, id=store_id)
    store.delete()
    return JsonResponse({'success': True})

# Summary endpoint to get counts for dashboard
def get_dashboard_stats(_):
    products_count = Product.objects.count()
    stores_count = Toko.objects.count()
    categories_count = Category.objects.count()
    return JsonResponse({
        'success': True,
        'products_count': products_count,
        'stores_count': stores_count,
        'categories_count': categories_count
    })