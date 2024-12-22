from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from productpage import models
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
import urllib.parse

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
        decoded_name = urllib.parse.unquote(product_name)
        product = get_object_or_404(Product, name=decoded_name)
    else:
        return render(request, '404.html', status=404)
    
    # Prepare a list to store matching stores
    matching_stores = list(product.store.all())

    # Fetch products in the same category, excluding the current product
    same_category_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:10]

    context = {
        'product': product,
        'same_category_products': same_category_products,
        'matching_stores': matching_stores,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    }

    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()
        context.update({'is_favorited': is_favorited})

    return render(request, 'product_detail.html', context)

def redirect_to_store(request, product_id, store_id):
    product = get_object_or_404(Product, id=product_id)
    store = product.store.filter(Toko, id=store_id)

    if store:
        return redirect('storepae:storedetail', store_id=store.id)

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

@csrf_exempt
@require_http_methods(["GET"])
def product_list_view(request):
    products = Product.objects.all().prefetch_related('ratings', 'category', 'store')
    product_list = []
    for product in products:
        ratings = []
        for rating in product.ratings.all():
            ratings.append({
                "model": "productpage.rating",
                "pk": rating.pk,
                "fields": {
                    "user": rating.user.username,
                    "product": str(product.id),
                    "rating": rating.rating,
                    "review": rating.review,
                    "created_at": rating.created_at.isoformat(),
                }
            })

        # Serialize stores
        stores = []
        for toko in product.store.all():
            stores.append({
                "model": "storepage.Toko",
                "pk": toko.pk,
                "fields": {
                    "nama": toko.nama,
                    "hari_buka": toko.hari_buka,
                    "alamat": toko.alamat,
                    "email": toko.email,
                    "telepon": toko.telepon,
                    "image": toko.image.name,
                    "gmaps_link": toko.gmaps_link,
                }
            })
        # Serialize product data
        product_data = {
            "model": "productpage.product",
            "pk": str(product.id),
            "fields": {
                "name": product.name,
                "category": category_json(product.category),
                "min_price": float(product.min_price),
                "max_price": float(product.max_price),
                "description": product.description,
                "store": stores,
                "image": product.image.name,
                "average_rating": product.count_average_rating(),
                "num_reviews": product.num_reviews(),
                "ratings": ratings,
            }
        }
        product_list.append(product_data)

    return JsonResponse(product_list, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def product_detail_flutter(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.ratings.all().order_by('-created_at')

    reviews_data = []
    for review in reviews:
        reviews_data.append({
                "model": "productpage.rating",
                "pk": review.pk,
                "fields": {
                    "user": review.user.username,
                    "product": str(product.id),
                    "rating": review.rating,
                    "review": review.review,
                    "created_at": review.created_at.isoformat(),
                }
            })

    # Serialize stores
        stores = []
        for toko in product.store.all():
            stores.append({
                "model": "storepage.Toko",
                "pk": toko.pk,
                "fields": {
                    "nama": toko.nama,
                    "hari_buka": toko.hari_buka,
                    "alamat": toko.alamat,
                    "email": toko.email,
                    "telepon": toko.telepon,
                    "image": toko.image.name,
                    "gmaps_link": toko.gmaps_link,
                }
            })

    data = {
            "model": "productpage.product",
            "pk": str(product.id),
            "fields": {
                "name": product.name,
                "category": category_json(product.category),
                "min_price": float(product.min_price),
                "max_price": float(product.max_price),
                "description": product.description,
                "store": stores,
                "image": product.image.name,
                "average_rating": product.count_average_rating(),
                "num_reviews": product.num_reviews(),
                "ratings": reviews_data,
            }
    }

    return JsonResponse(data)

@csrf_exempt
@require_http_methods(["POST"])
def add_review_flutter(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to add a review.")

    product = get_object_or_404(Product, pk=product_id)
    try:
        body = json.loads(request.body)
        rating = int(body.get('rating', 0))
        review_text = body.get('review', '')

        if rating < 1 or rating > 5:
            return JsonResponse({'error': 'Rating must be between 1 and 5.'}, status=400)

        review = Rating.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            review=review_text,
        )
        review.save()
        data = {
            "model": "productpage.rating",
            "pk": review.pk,
            "fields": {
                "user": review.user.username,
                "product": str(product.id),
                "rating": review.rating,
                "review": review.review,
                "created_at": review.created_at.isoformat(),
            }
        }
        return JsonResponse(data, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
@require_http_methods(["POST","GET"])
def edit_review_flutter(request, product_id, review_id):
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(Rating, pk=review_id, product=product)

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            rating = body.get('rating', review.rating)
            review_text = body.get('review', review.review)

            if not (1 <= rating <= 5):
                return JsonResponse({'error': 'Rating must be between 1 and 5.'}, status=400)

            review.rating = rating
            review.review = review_text.strip()
            
            review.save()

            data = {
                'pk': review.pk,
                'model': 'productpage.rating',
                'fields': {
                    'user': review.user.username,
                    'product': str(review.product.pk),
                    'rating': review.rating,
                    'review': review.review,
                    'created_at': review.created_at.isoformat(),
                }
            }

            return JsonResponse(data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def delete_review_flutter(request, product_id, review_id):
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(Rating, pk=review_id, product=product)

    review.delete()

    return JsonResponse({'message': 'Review deleted successfully.'}, status=200)

def category_json(category):
    return {
        "model": "productpage.category",
        "pk": category.pk,
        "fields": {
            "name": category.name,
        }
    }

@require_http_methods(["GET"])
def category_list_view(request):
    categories = Category.objects.all()
    category_list = []
    for category in categories:
        category_list.append({
            "model": "productpage.category",
            "pk": category.pk,
            "fields": {
                "name": category.name,
            }
        })
    return JsonResponse(category_list, safe=False)

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