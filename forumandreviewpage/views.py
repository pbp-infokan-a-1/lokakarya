from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from forumandreviewpage.forms import ForumandReviewForm, CommentForm
from forumandreviewpage.models import PostForum, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from userprofile.models import Activity
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def show_forum(request):
    posts = PostForum.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'forumandreviewpage.html', context)

@login_required(login_url='/login')
def create_forum_entry(request):
    if request.method == "POST":
        form = ForumandReviewForm(request.POST)
        if form.is_valid():
            forum_entry = form.save(commit=False)
            forum_entry.author = request.user
            forum_entry.save()

            # Log the activity
            Activity.objects.create(
                user=request.user,
                action="just made a forum",
                related_url=reverse('forumandreviewpage:detail_post', kwargs={'post_id': forum_entry.id})
            )

            return redirect('forumandreviewpage:show_forum')
    else:
        form = ForumandReviewForm()
    return render(request, "create_forum_entry.html", {'form': form})

@login_required
def detail_post(request, post_id):
    post = get_object_or_404(PostForum, id=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # Log the activity
            Activity.objects.create(
                user=request.user,
                action="just commented on a forum",
                related_url=reverse('forumandreviewpage:detail_post', kwargs={'post_id': post.id})
            )
            
            return redirect('forumandreviewpage:detail_post', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'detail_post.html', {'post': post, 'comment_form': comment_form})

@login_required 
def upvote_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(PostForum, id=post_id)
        # Tambahkan user ke relasi upvotes
        post.upvotes.add(request.user)
        Activity.objects.create(
                user=request.user,
                action="just upvote on a forum",
                related_url=reverse('forumandreviewpage:detail_post', kwargs={'post_id': post.id})
            )
        # Update total upvotes
        post.total_upvotes = post.calculate_total_upvotes()
        post.save()
        return redirect('forumandreviewpage:show_forum')

@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(PostForum, id=post_id)
        post.delete()
        return HttpResponseRedirect(reverse('forumandreviewpage:show_forum'))

def edit_post(request, post_id):
    post = get_object_or_404(PostForum, id=post_id)

    if post.author != request.user:
        return redirect('forumandreviewpage:show_forum')

    if request.method == 'POST':
        form = ForumandReviewForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            Activity.objects.create(
                user=request.user,
                action="just edit on a forum",
                related_url=reverse('forumandreviewpage:detail_post', kwargs={'post_id': post.id})
            )
            return redirect('forumandreviewpage:detail_post', post_id=post.id)
    else:
        form = ForumandReviewForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

@csrf_exempt
@require_POST
def edit_post_ajax(request, post_id):
    # Get the new data from the POST request
    title = request.POST.get("title")
    content = request.POST.get("content")
    
    # Get the mood entry object, or return 404 if not found
    forum_entry = get_object_or_404(PostForum, id=post_id, author=request.user)
    
    # Update the mood entry with the new data
    forum_entry.title = title
    forum_entry.content = content
    forum_entry.save()  # Save the updated entry
    
    return HttpResponse(b"UPDATED", status=200)

def show_xml(request):
    data = PostForum.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = PostForum.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = PostForum.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = PostForum.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_forum_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user  # Ambil user dari sesi atau autentikasi
            title = data.get('title', '')
            content = data.get('content', '')

            # Validasi input
            if not title or not content:
                return JsonResponse({"status": "error", "message": "Title or content cannot be empty"}, status=400)

            # Buat forum baru, gunakan 'author' karena itu nama field di model
            new_forum = PostForum.objects.create(
                author=user,  # Gunakan 'author' di sini
                title=title,
                content=content,
            )
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
@csrf_exempt
@login_required
def edit_forum_flutter(request, forum_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            forum = PostForum.objects.get(id=forum_id)

            # Verifikasi apakah user yang sedang login adalah pemilik postingan
            if forum.user != request.user:
                return JsonResponse({"status": "error", "message": "You are not authorized to edit this forum."}, status=403)

            # Update forum
            forum.title = data.get("title", forum.title)
            forum.content = data.get("content", forum.content)
            forum.save()

            return JsonResponse({"status": "success", "message": "Forum updated successfully."}, status=200)
        except PostForum.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Forum not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt
@login_required
def delete_forum_flutter(request, forum_id):
    if request.method == 'DELETE' or request.headers.get('X-HTTP-Method-Override') == 'DELETE':
        try:
            forum = PostForum.objects.get(id=forum_id)
            if forum.user != request.user:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
            forum.delete()
            return JsonResponse({"status": "success"}, status=200)
        except PostForum.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Not found"}, status=404)
    return JsonResponse({"status": "error"}, status=405)

@csrf_exempt
@login_required
def upvote_forum_flutter(request, forum_id):
    if request.method == 'POST':
        try:
            forum = PostForum.objects.get(id=forum_id)
            if request.user.id in forum.upvotes:
                return JsonResponse({"status": "error", "message": "Already upvoted"}, status=400)
            forum.upvotes.append(request.user.id)
            forum.total_upvotes += 1
            forum.save()
            return JsonResponse({"status": "success", "upvotes": forum.total_upvotes}, status=200)
        except PostForum.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Not found"}, status=404)
    return JsonResponse({"status": "error"}, status=405)

def post_comment_json(request):
    forums = PostForum.objects.all().select_related('author')
    response_data = []
    for forum in forums:
        response_data.append({
            "model": "forum.postforum",
            "pk": forum.id,
            "fields": {
                "title": forum.title,
                "content": forum.content,
                "author": forum.author.id,
                "author_name": forum.author.username if forum.author else "Unknown",
                "created_at": forum.created_at.isoformat(),
                "total_upvotes": forum.total_upvotes,
                "upvotes": list(forum.upvotes.values_list('id', flat=True)),
                "comments": [
                    {
                        "id": comment.id,
                        "content": comment.content,
                        "author_name": comment.author.username if comment.author else "Anonymous",
                        "created_at": comment.created_at.isoformat(),
                    }
                    for comment in forum.comments.all()
                ] if forum.comments.exists() else [],
            },
        })
    return JsonResponse(response_data, safe=False)

@csrf_exempt
def login_flutter(request):
    if request.method == 'POST':
        try:
            # Parse JSON dari request body
            body = json.loads(request.body)
            username = body.get('username', '')
            password = body.get('password', '')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login user dan buat session
                login(request, user)

                # Kirim respons dengan data user
                return JsonResponse({
                    "status": True,
                    "message": "Successfully Logged In!",
                    "username": user.username,
                    "is_superuser": user.is_superuser,
                    "sessionid": request.session.session_key,  # Session ID untuk autentikasi lanjutan
                    "user_id": user.id,  # Kirim user ID untuk Flutter
                }, status=200)
            else:
                # Jika login gagal
                return JsonResponse({
                    "status": False,
                    "message": "Invalid login credentials!",
                }, status=401)

        except json.JSONDecodeError:
            # Jika JSON yang dikirimkan tidak valid
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON format!",
            }, status=400)
    else:
        # Jika method selain POST digunakan
        return JsonResponse({
            "status": False,
            "message": "Method not allowed!",
        }, status=405)