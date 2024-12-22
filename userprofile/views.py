from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from userprofile.models import Profile, Status, Activity
from .forms import ProfileForm, StatusForm
from django.core import serializers
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
import json
from datetime import datetime

@login_required
def profile(request, username):
    # Get the user based on the username in the URL
    user = get_object_or_404(User, username=username)

    try:
        user_profile = user.profile  # Access the profile of the user
    except Profile.DoesNotExist:
        # If the profile doesn't exist, you can create it or handle the error
        user_profile = Profile.objects.create(user=user)

    # Fetch the user's recent activities
    activities = Activity.objects.filter(user=user).order_by('-timestamp')
    last_login_cookie = request.COOKIES.get('last_login', None)
    
    context = {
        'profile': user_profile,
        'last_login': last_login_cookie,
        'is_owner': request.user == user,  # Check if the logged-in user owns this profile
        'activities': activities,
    }
    
    return render(request, 'profile.html', context)

@csrf_exempt
@login_required
def update_profile_ajax(request, username):
    # Check authentication first
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Authentication required',
            'authenticated': False
        }, status=401)

    user = get_object_or_404(User, username=username)

    # For GET request, return the user's profile data as JSON
    if request.method == "GET":
        try:
            profile = user.profile
            profile_data = {
                "username": user.username,
                "bio": profile.bio or "",
                "location": profile.location or "",
                "birth_date": profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else "",
                "private": profile.private or False,
                "authenticated": True
            }
            return JsonResponse(profile_data)
        except Profile.DoesNotExist:
            return JsonResponse({
                "username": user.username,
                "bio": "",
                "location": "",
                "birth_date": "",
                "private": False,
                "authenticated": True
            })
        except Exception as e:
            print(f"Error in update_profile_ajax: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "UPDATED"}, status=200)
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)

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

def show_json_profile(request):
    data = Profile.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@csrf_exempt
def update_profile_app(request, username):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get the user's profile
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            
            # Update the profile fields
            profile.bio = data.get('bio', '')
            profile.location = data.get('location', '')
            profile.birth_date = datetime.strptime(data.get('birth_date', ''), '%Y-%m-%d').date()
            profile.private = data.get('private', False)
            
            # Save the changes
            profile.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Profile updated successfully!"
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "User not found."
            }, status=404)
            
        except Profile.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Profile not found."
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
            
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)

@csrf_exempt
def create_status_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = Status.objects.create(
            user=request.user,
            title=data["title"],
            description=data["description"]
        )

        new_status.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
