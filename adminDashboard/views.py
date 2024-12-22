from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .forms import TokoForm, ProductForm
from storepage.models import Toko
from productpage.models import Product, Category
import logging

logger = logging.getLogger(__name__)

@login_required
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
    page = int(request.GET.get('page', 1))
    per_page = 10
    products = Product.objects.all()[(page-1)*per_page:page*per_page]
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
@staff_member_required
@require_http_methods(["POST"])
def add_product(request):
    try:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()
            return JsonResponse({'success': True, 'product': product.to_dict()})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(["GET", "POST"])
def edit_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'product': product.to_dict()})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
        # GET request - return product data for form population
        return JsonResponse({
            'success': True,
            'product': product.to_dict()
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Error editing product: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def delete_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def store_list(_):
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
@staff_member_required
@require_http_methods(["POST"])
def add_store(request):
    try:
        form = TokoForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save()
            return JsonResponse({'success': True, 'store': store.to_dict()})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except Exception as e:
        logger.error(f"Error adding store: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(["GET", "POST"])
def edit_store(request, store_id):
    try:
        store = get_object_or_404(Toko, id=store_id)
        if request.method == 'POST':
            form = TokoForm(request.POST, request.FILES, instance=store)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'store': store.to_dict()})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
        # GET request - return store data for form population
        return JsonResponse({
            'success': True,
            'store': store.to_dict()
        })
    except Toko.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Store not found'}, status=404)
    except Exception as e:
        logger.error(f"Error editing store: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def delete_store(request, store_id):
    try:
        store = get_object_or_404(Toko, id=store_id)
        store.delete()
        return JsonResponse({'success': True, 'message': 'Store deleted successfully'})
    except Toko.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Store not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting store: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
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

@login_required
def is_superuser(request):
    return JsonResponse({'is_superuser': request.user.is_superuser})