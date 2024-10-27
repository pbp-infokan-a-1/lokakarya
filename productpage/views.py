from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from productpage.models import Product, Rating, Category, Favorite
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from storepage.models import Toko
from .forms import RatingForm
from django.utils import timezone
import json
from django.core import serializers
from userprofile.models import Activity

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
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'product_page.html', context)

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, product_id):
    data = get_object_or_404(Product, id=product_id)
    return HttpResponse(serializers.serialize("json", [data]), content_type="application/json")

# Product details
def product_detail(request, product_id=None, product_name=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    elif product_name:
        product = get_object_or_404(Product, name=product_name)
    else:
        return render(request, '404.html', status=404)
    
    # Prepare a list to store matching stores
    matching_stores = list(product.store.all())

    # Fetch products in the same category, excluding the current product
    same_category_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:5]

    is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'same_category_products': same_category_products,
        'matching_stores': matching_stores,
        'is_favorited': is_favorited,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    }

    return render(request, 'product_detail.html', context)

@csrf_exempt
@login_required
def add_review_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            review_text = data.get('review')
            review_rating = data.get('rating')

            Rating.objects.create(
                product=product,
                user=request.user,
                review=review_text,
                rating=float(review_rating)
            )

            return JsonResponse({"message": "Review added successfully!"}, status=200)

        except ValueError:
            return JsonResponse({"error": "Invalid data"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

def product_reviews(request, product_id):
    page = request.GET.get('page', 1)
    reviews = Rating.objects.filter(product_id=product_id).order_by('-created_at')
    paginator = Paginator(reviews, 5)  # Show 5 reviews per page

    reviews_list = []
    for review in paginator.get_page(page):
        reviews_list.append({
            'username': review.user.username,
            'profile_pic': review.user.profile_pic.url if review.user.profile_pic else '/default/path/to/avatar.jpg',
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M'),
            'rating': review.rating,
            'comment': review.comment,
        })

    data = {
        'reviews': reviews_list,
        'has_next': paginator.get_page(page).has_next(),
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
def edit_review_ajax(request, product_id, review_id):
    try:
        review = get_object_or_404(Rating, id=review_id, user=request.user, product_id=product_id)

        if request.method == "POST":
            data = json.loads(request.body)
            review_text = data.get('review', '')
            review_rating = data.get('rating', 0)

            review.review = review_text
            review.rating = float(review_rating)
            review.save()

            return JsonResponse({"message": "Review updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)
    except Rating.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
    except ValueError:
        return JsonResponse({"error": "Invalid data"}, status=400)
    except Exception as e:
        print(e)  # For debugging purposes
        return JsonResponse({"error": "Internal server error"}, status=500)

@csrf_exempt
@login_required
def delete_review_ajax(request, product_id, review_id):
    try:
        review = get_object_or_404(Rating, id=review_id, user=request.user, product_id=product_id)

<<<<<<< HEAD
        if request.method == "DELETE":
            review.delete()
            return JsonResponse({"message": "Review deleted successfully!"}, status=200)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)
    except Rating.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
    except Exception as e:
        print(e)  # For debugging purposes
        return JsonResponse({"error": "Internal server error"}, status=500)
=======
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.min_price = data.get('min_price', product.min_price)
            product.max_price = data.get('max_price', product.max_price)

            category_id = data.get('category')
            if category_id:
                category = get_object_or_404(Category, id=category_id)
                product.category = category

            product.save()
            return JsonResponse({"message": "Product updated successfully!"}, status=200)

        except ValueError:
            return JsonResponse({"error": "Invalid data"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@login_required
def delete_product_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({"message": "Product deleted successfully!"}, status=204)

    return JsonResponse({"error": "Method not allowed"}, status=405)

def is_admin(user):
    return user.groups.filter(role='Admin').exists()
>>>>>>> 5ce3ae1d1228c1224f3e327884cb819562d3430a

@login_required
def favorite_page(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if 'add' in request.POST:
            # Add to favorites
            Favorite.objects.create(user=request.user, product=product)

            # Log the activity
            Activity.objects.create(
                user=request.user,
                action=f"just added {product.name} as favorite",
                related_url=reverse('productpage:product_detail', kwargs={'product_id': product.id})
            )

        elif 'remove' in request.POST:
            # Remove from favorites
            Favorite.objects.filter(user=request.user, product=product).delete()

            # Log the activity
            Activity.objects.create(
                user=request.user,
                action=f"just removed {product.name} from favorites",
                related_url=reverse('productpage:product_detail', kwargs={'product_id': product.id})
            )

    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_page.html', {'favorites': favorites})