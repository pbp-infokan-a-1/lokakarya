import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from productpage.models import Favorite, Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="/login")
@require_POST
def toggle_favorite(request, product_id):
    # Retrieve the product
    product = get_object_or_404(Product, pk=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product).first()

    if favorite:
        # If the product is already in favorites, remove it
        favorite.delete()
        messages.success(request, "Product removed from favorites.")
        print("Product removed from favorites.")
        return JsonResponse(
            {
                "success": True,
                "message": "Removed from favorites!",
                "is_favorited": False,
            }
        )
    else:
        # If the product is not in favorites, add it
        print("Product added to favorites.")
        Favorite.objects.create(user=request.user, product=product)
        messages.success(request, "Product added to favorites!")
        return JsonResponse(
            {"success": True, "message": "Added to favorites!", "is_favorited": True}
        )


@login_required(login_url="/login")
def view_all_favorites_by_user(request):
    # Retrieve all favorites for the logged-in user
    favorites = Favorite.objects.filter(user=request.user).select_related("product")
    context = {
        "favorites": favorites,
    }
    return JsonResponse({"favorites": favorites})


@login_required(login_url="/login")
def view_all_favorites_by_user_id(request, user_id):
    # Only allow admin or the user themselves to view favorites
    if request.user.is_staff or request.user.id == user_id:
        user = get_object_or_404(User, pk=user_id)
        favorites = Favorite.objects.filter(user=user).select_related("product")
        context = {
            "favorites": favorites,
            "viewing_user": user,
        }
        return JsonResponse({"favorites": favorites, "viewing_user": user})

    else:
        return HttpResponseForbidden(
            "You do not have permission to view this user's favorites."
        )


def test(request):
    return HttpResponseForbidden("testing")

def show_json_favorites(request):
    # Retrieve all favorites for the logged-in user
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated."}, status=401)

    favorites = Favorite.objects.filter(user=request.user).select_related("product")
    data = [
        {
            "id": favorite.product.id,
          
        }
        for favorite in favorites
    ]
    return JsonResponse({"favorites": data})


@csrf_exempt  
def add_favorite_flutter(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User is not authenticated."}, status=401)
        
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            if not product_id:
                return JsonResponse({"status": "error", "message": "Product ID is required."}, status=400)
            
            product = Product.objects.get(id=product_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
          

            if created:
                return JsonResponse({"status": "success", "message": "Product added to favorites."}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Product is already in favorites."}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt  
def remove_favorite_flutter(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User is not authenticated."}, status=401)
        
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            if not product_id:
                return JsonResponse({"status": "error", "message": "Product ID is required."}, status=400)
            
            favorite = Favorite.objects.get(user=request.user, product__id=product_id)
            favorite.delete()
            
            return JsonResponse({"status": "success", "message": "Product removed from favorites."}, status=200)
        
        except Favorite.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Favorite does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)