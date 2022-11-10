from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from .forms import *

# Create your views here.
def review_index(request):
    reviews = Review.objects.order_by("-pk")
    context = {
        "reviews" : reviews,
    }
    return render(request, "articles/review_index.html", context)

def review_create(request):
    # article = Article.objects.get(pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # review.user = request.user
            review.save()
            return redirect("articles:review_index")
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "articles/review_create.html", context)


def review_detail(request, pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=pk)
    context = {
        "review": review,
    }
    return render(request, "articles/review_detail.html", context)


def review_delete(request, pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=pk)
    if request.user != review.user:
        return redirect("articles:review_index")
    if request.method == "POST":
        if request.user == review.user:
            review.delete()
            return redirect("articles:review_index")
    else:
        return redirect("articles:review_index", pk)


def review_update(request, pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        images = request.FILES.getlist("image")
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.save()
            return redirect("articles:review_detail")
    else:
        review_form = ReviewForm(instance=review)
    context = {
        "review_form": review_form,
    }
    return render(request, "articles/review_create.html", context)


def review_like(request, pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        is_liked = False
    else:
        review.like_users.add(request.user)
        is_liked = True
    data = {
        "isLiked": is_liked,
        "likeCount": review.like_users.count(),
    }
    return JsonResponse(data)