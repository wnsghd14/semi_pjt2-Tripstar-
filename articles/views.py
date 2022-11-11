from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm, ReviewForm, PhotoForm
from .models import Article, Review, Comment, Photo
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request, 'articles/index.html', context)


@login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            # accounts 연결 후에
            article = article_form.save(commit=False)
            article.user = request.user
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form':article_form,
    }
    return render(request, 'articles/create.html', context)


def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    reviews = Review.objects.filter(article=article)
    context = {
        'article':article,
        'reviews':reviews,
    }
    return render(request, 'articles/detail.html', context)



@login_required
def update(request, articles_pk):
    article = get_object_or_404(Article, pk=articles_pk)
    # 로그인한 유저와 작성한 유저가 같다면
    if request.user == article.user:
        if request.method == "POST":
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                return redirect('articles:detail', articles_pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form' :article_form,
        }
        return render(request, 'articles/update.html', context)

    # 작성자가 아닐 경우
    else:
        return redirect('articles:detail', articles_pk)
    

# @login_required
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()

    return redirect('articles:index')


def review_index(request):
    reviews = Review.objects.order_by("-pk")
    context = {
        "reviews" : reviews,
    }
    return render(request, "articles/review_index.html", context)


def review_create(request,article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            if len(images):
                for image in images:
                    image_instance = Photo(review=review, image=image)
                    review.article = article
                    review.save()
                    image_instance.save()
            review.article = article
            review.save()
            return redirect("articles:detail", article_pk)
    else:
        review_form = ReviewForm()
        photo_form = PhotoForm()
    context = {
        "review_form": review_form,
        "photo_form": photo_form,
    }
    return render(request, "articles/review_create.html", context)


def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form":comment_form,
        "comments": review.comment_set.all(),
        "photo_cnt": review.photo_set.count(),
    }
    return render(request, "articles/review_detail.html", context)


def review_delete(request, review_pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        if request.user == review.user:
            review.delete()
            return redirect("articles:detail", review.article.pk)
    else:
        return redirect("articles:detail", review.article.pk)


def review_update(request, review_pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=review_pk)
    photos = Photo.objects.filter(review_id=review.pk)
    
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")

        for photo in photos:
            if photo.image:
                photo.delete()
        
        if review_form.is_valid() and photo_form.is_valid():
            review = review_form.save(commit=False)
            if len(images):
                for image in images:
                    image_instance = Photo(review=review, image=image)
                    review.save()
                    image_instance.save()
            review.save()
            return redirect("articles:review_detail", review.pk)
    else:
        review_form = ReviewForm(instance=review)
        if photos:
            photo_form = PhotoForm(instance=photos[0])
        else:
            photo_form = PhotoForm()

    context = {
        "review_form": review_form,
        "photo_form": photo_form,
    }
    return render(request, "articles/review_create.html", context)


def review_like(request, review_pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=review_pk)
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
    

def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("articles:review_detail", review_pk)


def comment_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
            return redirect("reviews:review_detail", review_pk)
    else:
        return HttpResponseForbidden()

def search(request):
    articles = None
    reviews = None
    users = None
    query = None
    if "q" in request.GET:
        query = request.GET.get("q")
        articles = Article.objects.order_by("-pk").filter(
            Q(title__contains=query) | Q(content__contains=query)
        )
        reviews = Review.objects.order_by("-pk").filter(
            Q(title__contains=query) | Q(content__contains=query)
        )
        users = get_user_model().objects.order_by("-pk").filter(username__contains=query)
    context = {
        "query": query,
        "articles": articles,
        "reviews": reviews,
        "users": users,
    }
    return render(request, "articles/search.html", context)