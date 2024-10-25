from django.shortcuts import render, get_object_or_404, redirect
from productpage.models import Product, Rating, Category, Favorite
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Product listing with category filters
def product_page(request):
    categories = Category.objects.all()  # Get all categories
    selected_categories = request.GET.getlist('category')
    products = Product.objects.all()

    # Filter products by selected categories
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # Search products by name
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Prefetch the average rating and number of reviews for each product
    products = products.annotate(
        average_rating=Avg('ratings__rating'),
        num_reviews=Count('ratings')
    )

    selected_category = None
    if selected_categories:
        selected_category = Category.objects.filter(id=selected_categories[0]).first()

    context = {
        'products': products,
        'categories': categories,
        'selected_categories': selected_categories,
        'query': query,
        'selected_category': selected_category,
    }
    return render(request, 'product_page.html', context)

# Product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ratings = product.ratings.all()

    # Calculate the average rating
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = ratings.count()

    return render(request, 'product_detail.html', {
        'product': product,
        'average_rating': average_rating,
        'total_reviews': total_reviews
    })

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
