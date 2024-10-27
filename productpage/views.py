from django.shortcuts import render, get_object_or_404, redirect
from productpage.models import Product, Rating, Category, Favorite
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from storepage.models import Toko

# Product listing with category filters
def product_page(request):
    categories = Category.objects.all()  # Get all categories
    selected_categories = request.GET.getlist('category')
    products = Product.objects.all()

    # Filter products by selected categories
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # Search products by name
    query = request.GET.get('q','')
    if query:
        products = products.filter(name__icontains=query)

    selected_category = None
    if selected_categories:
        selected_category = Category.objects.filter(id=selected_categories[0]).first()

    # Pagination setup
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'query': query,
        'selected_category': selected_category,
    }
    return render(request, 'product_page.html', context)

# Product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Prepare a list to store matching stores
    matching_stores = list(product.store.all())

    # Fetch products in the same category, excluding the current product
    same_category_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:5]

    is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()

    return render(request, 'product_detail.html', {
        'product': product,
        'same_category_products': same_category_products,
        'matching_stores': matching_stores,
        'is_favorited': is_favorited,
    })

#incomplete
def submit_rating(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        Rating.objects.update_or_create(user=request.user, product=product, defaults={'rating': rating})
        
        # Update product rating
        all_ratings = Rating.objects.filter(product=product)
        # product.rating = all_ratings.aggregate(models.Avg('rating'))['rating__avg']
        product.num_reviews = all_ratings.count()
        product.save()
        
    return redirect('product_detail', product_id=product.id)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user == product.store.owner or is_admin(request.user):
        product.delete()
        return redirect('product_list')
    else:
        return HttpResponseForbidden("You are not allowed to delete this product.")

def is_admin(user):
    return user.groups.filter(role='Admin').exists()

@login_required
def favorite_page(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites': favorites
    }
    return render(request, 'favorite_page.html', context)