from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from productpage.models import Product
from userprofile.models import Profile
from storepage.models import Toko
from django.http import JsonResponse

# Unified search across Products, Stores, and Profiles
def search(request):
    query = request.GET.get('q', '')  # Get the search term from the query parameter
    selected_category = None
    
    products = profiles = None  # Initialize as None
    
    # If there is a query, search through Products, Stores, and Profiles
    if query:
        # Search Products by name or description
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        stores = Toko.objects.filter(Q(nama__icontains=query)) 
        # Search Profiles by username or bio
        profiles = Profile.objects.filter(Q(user__username__icontains=query) | Q(bio__icontains=query))
    
    context = {
        'query': query,
        'products': products,
        'stores' : stores,
        'profiles': profiles,
        'selected_category': selected_category
    }
    
    return render(request, 'search_results.html', context)

def home(request):
    return render(request, 'main.html')

def search_mobile(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'error': 'No query provided'})

    try:
        # Search products with complete data
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).select_related('category').prefetch_related('ratings')[:5]

        # Format products safely
        formatted_products = []
        for product in products:
            try:
                formatted_products.append({
                    'model': 'productpage.product',
                    'pk': str(product.pk),
                    'fields': {
                        'name': product.name or '',
                        'description': product.description or '',
                        'category': {
                            'model': 'productpage.category',
                            'pk': product.category.pk if product.category else 0,
                            'fields': {
                                'name': product.category.name if product.category else '',
                            }
                        },
                        'min_price': 0,
                        'max_price': 0,
                        'store': [],
                        'image': str(product.image) if product.image else '',
                        'average_rating': float(product.count_average_rating() or 0),
                        'num_reviews': product.ratings.count(),
                        'ratings': [
                            {
                                'model': 'productpage.rating',
                                'pk': rating.pk,
                                'fields': {
                                    'rating': float(rating.rating or 0),
                                    'review': rating.review or '',
                                    'user': rating.user.username if rating.user else '',
                                }
                            } for rating in product.ratings.all()
                        ],
                    }
                })
            except Exception as e:
                print(f"Error formatting product {product.pk}: {str(e)}")
                continue

        # Search stores with complete data
        stores = Toko.objects.filter(
            Q(nama__icontains=query) |
            Q(alamat__icontains=query) |
            Q(email__icontains=query)
        )[:5]

        # Format stores safely
        formatted_stores = []
        for store in stores:
            try:
                formatted_stores.append({
                    'id': store.id,
                    'nama': store.nama or '',
                    'hari_buka': store.hari_buka or 'Senin-Jumat',
                    'alamat': store.alamat or '',
                    'email': store.email or '',
                    'telepon': store.telepon or '',
                    'image': store.image.url if hasattr(store, 'image') and store.image else '',
                    'gmaps_link': store.gmaps_link or '',
                })
            except Exception as e:
                print(f"Error formatting store {store.id}: {str(e)}")
                continue

        # Search profiles
        profiles = Profile.objects.filter(
            Q(user__username__icontains=query) |
            Q(bio__icontains=query) |
            Q(location__icontains=query)
        ).select_related('user')[:5]

        # Format profiles safely
        formatted_profiles = []
        for profile in profiles:
            try:
                formatted_profiles.append({
                    'username': profile.user.username if profile.user else '',
                    'bio': profile.bio or '',
                })
            except Exception as e:
                print(f"Error formatting profile {profile.pk}: {str(e)}")
                continue

        return JsonResponse({
            'products': formatted_products,
            'stores': formatted_stores,
            'profiles': formatted_profiles,
        })

    except Exception as e:
        print(f"Search error: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred while searching',
            'products': [],
            'stores': [],
            'profiles': [],
        })
