from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    recommended_reviews = Review.objects.order_by('-total_helpful')[:3]

    return render(request, 'review_list.html', {'reviews': reviews, 'recommended_reviews': recommended_reviews})

@login_required(login_url='/login')
def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_entry = form.save(commit=False)
            review_entry.author = request.user
            review_entry.save()
            return redirect('reviewpage:review_list')
    else:
        form = ReviewForm()
    return render(request, "create_review.html", {'form': form})

@csrf_exempt
def delete_review(request, review_id):
    if request.method == 'GET':
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return HttpResponseRedirect(reverse('reviewpage:review_list'))

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.author != request.user:
        return redirect('reviewpage:review_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviewpage:review_list')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required 
def helpful_review(request, review_id):
    if request.method == 'POST':
        post = get_object_or_404(Review, id=review_id)
        post.helpful.add(request.user)
        post.total_helpful = post.calculate_total_helpful()
        post.save()
        return redirect('reviewpage:review_list')
    
@login_required
def unhelpful_review(request, review_id):
    if request.method == 'POST':
        post = get_object_or_404(Review, id=review_id)
        post.unhelpful.add(request.user)
        post.total_unhelpful = post.calculate_total_unhelpful()
        post.save()
        return redirect('reviewpage:review_list')