from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from userprofile.models import Profile, Status
from .forms import ProfileForm, StatusForm
from django.core import serializers

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

@csrf_exempt
def update_profile_ajax(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "UPDATED"}, status=200)
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)

    # For GET request, return the user's profile data as JSON
    if request.method == "GET":
        profile = request.user.profile
        profile_data = {
            "username": request.user.username,
            "bio": profile.bio,
            "location": profile.location,
            "birth_date": profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else None
        }
        return JsonResponse(profile_data, status=200)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@require_POST
def update_status_ajax(request):
    title = strip_tags(request.POST.get("title"))
    description = strip_tags(request.POST.get("description"))
    user = request.user

    new_status = Status(
        title=title, description=description, user=user
    )
    new_status.save()

    return HttpResponse(b"CREATED", status=201)

def status_json(request):
    data = Status.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_status(request, id):
    # Get item entry berdasarkan id
    status = Status.objects.get(pk = id)

    # Set item entry sebagai instance dari form
    form = StatusForm(request.POST or None, instance=status)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('userprofile:profile'))

    context = {'form': form}
    return render(request, "edit_status.html", context)

def delete_status(request, id):
    # Get item berdasarkan id
    status = Status.objects.get(pk = id)
    # Hapus item
    status.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('userprofile:profile'))