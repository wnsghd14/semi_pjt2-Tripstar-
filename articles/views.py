from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm, ReviewForm
from .models import Article, Review, Comment, Review
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseForbidden

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')

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


def detail(request, articles_pk):
    article = get_object_or_404(Article, pk=articles_pk)
    context = {
        'article':article,
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
    
@login_required
def delete(request, articles_pk):
    article = get_object_or_404(Article, pk=articles_pk)
    article.delete()
    return redirect('articles:index')

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
    
def comment_create(request,pk):
    review = get_object_or_404(Review,pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("articles:reviews_detail",review.pk)

def comment_update(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("articles:reviews_detail",request.user.pk)
    else:
        return HttpResponseForbidden()

def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
            return redirect("reviews:detail", pk)
    else:
        return HttpResponseForbidden()

