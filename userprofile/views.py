from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userprofile.models import Profile
from .forms import ProfileForm

@login_required
def update_profile(request):
    profile = request.user.profile
    last_login_cookie = request.COOKIES.get('last_login', None)  # Safely get the last_login cookie
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile:profile')  # Redirect to landing page after update
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'last_login': last_login_cookie
    }
    return render(request, 'update_profile.html', context)

@login_required
def profile(request):
    try:
        user_profile = request.user.profile  # Try to access the user's profile
    except Profile.DoesNotExist:
        # If the profile doesn't exist, create a new profile for the user
        user_profile = Profile.objects.create(user=request.user)
    
    last_login_cookie = request.COOKIES.get('last_login', None)  # Safely get the last_login cookie

    context = {
        'profile': user_profile,
        'last_login': last_login_cookie
    }
    return render(request, 'profile.html', context)
