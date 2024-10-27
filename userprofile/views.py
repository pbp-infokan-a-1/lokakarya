from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from userprofile.models import Profile, Status
from .forms import ProfileForm, StatusForm
from django.core import serializers
from django.contrib.auth.models import User

@login_required
def profile(request, username):
    # Get the user based on the username in the URL
    user = get_object_or_404(User, username=username)

    try:
        user_profile = user.profile  # Access the profile of the user
    except Profile.DoesNotExist:
        # If the profile doesn't exist, you can create it or handle the error
        user_profile = Profile.objects.create(user=user)

    last_login_cookie = request.COOKIES.get('last_login', None)

    context = {
        'profile': user_profile,
        'last_login': last_login_cookie,
        'is_owner': request.user == user  # Check if the logged-in user owns this profile
    }
    return render(request, 'profile.html', context)

@csrf_exempt
@login_required
def update_profile_ajax(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "UPDATED"}, status=200)
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)

    # For GET request, return the user's profile data as JSON
    if request.method == "GET":
        profile = user.profile
        profile_data = {
            "username": user.username,
            "bio": profile.bio,
            "location": profile.location,
            "birth_date": profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else None
        }
        return JsonResponse(profile_data, status=200)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@require_POST
@login_required
def update_status_ajax(request, username):
    user = get_object_or_404(User, username=username)
    
    title = strip_tags(request.POST.get("title"))
    description = strip_tags(request.POST.get("description"))

    new_status = Status(
        title=title, description=description, user=user
    )
    new_status.save()

    return HttpResponse(b"CREATED", status=201)

@login_required
def status_json(request, username):
    user = get_object_or_404(User, username=username)
    data = Status.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def status_json_by_id(request, status_id):
    data = Status.objects.filter(pk=status_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_status(request, status_id):
    # Get the status entry based on id
    status = Status.objects.get(pk=status_id)

    # Set the status entry as an instance of the form
    form = StatusForm(request.POST or None, instance=status)

    if form.is_valid() and request.method == "POST":
        # Save the form and redirect to the user's profile
        form.save()
        return HttpResponseRedirect(reverse('userprofile:profile', kwargs={'username': status.user.username}))

    context = {'form': form}
    return render(request, "edit_status.html", context)

def delete_status(request, status_id):
    # Get the status based on id
    status = Status.objects.get(pk=status_id)
    
    # Delete the status
    status.delete()

    # Redirect back to the user's profile
    return HttpResponseRedirect(reverse('userprofile:profile', kwargs={'username': status.user.username}))

