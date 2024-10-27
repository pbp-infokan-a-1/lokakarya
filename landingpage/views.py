from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from productpage.models import Product
from userprofile.models import Profile
from storepage.models import Toko

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
