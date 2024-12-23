from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth.models import User
import json

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Simpan user baru ke database
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login')  # Redirect ke halaman login setelah sukses
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("landingpage:home"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
      else:
        messages.error(request, "Invalid username or password. Please try again.")

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect("/")
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def login_app(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            session_id = request.session.session_key
            response = JsonResponse({
                "status": True,
                "message": "Successfully Logged In!",
                "username": user.username,
                "is_superuser": user.is_superuser,
                "sessionid": session_id,
            }, status=200)
            response.set_cookie(
                'sessionid',
                session_id,
                httponly=True,
                samesite='None',
                secure=True
            )
            return response
    return JsonResponse({
        "status": False,
        "message": "Failed to Login, check your email/password."
    }, status=401)

@csrf_exempt
def register_app(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout_app(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)