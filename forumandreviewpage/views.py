from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from forumandreviewpage.forms import ForumandReviewForm, CommentForm
from forumandreviewpage.models import PostForum, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request, "forumandreviewpage/create_forum_entry.html", {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(PostForum, id=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'forum/post_detail.html', {'post': post, 'comment_form': comment_form})

@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(PostForum, id=post_id)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    else:
        post.upvotes.add(request.user)
    return redirect('post_detail', post_id=post.id)

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
