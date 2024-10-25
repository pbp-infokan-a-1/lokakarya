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
            return redirect('detail_post', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'detail_post.html', {'post': post, 'comment_form': comment_form})

@login_required
def upvote_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(PostForum, id=post_id)
        post.total_upvotes += 1  # Increment the upvote count
        post.save()  # Save the updated post
        return HttpResponseRedirect(reverse('forumandreviewpage:index'))
    #     return JsonResponse({'success': True, 'total_upvotes': post.total_upvotes}, status=200)
    # return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(PostForum, id=post_id)
        post.delete()
        return HttpResponseRedirect(reverse('forumandreviewpage:show_forum'))

def edit_post(request, post_id):
    post = get_object_or_404(PostForum, id=post_id)
    if request.method == 'POST':
        form = ForumandReviewForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detail_post', post_id=post.id)
    else:
        form = ForumandReviewForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

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
