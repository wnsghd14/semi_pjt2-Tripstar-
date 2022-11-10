
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, Review,Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseForbidden

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')

# @login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            # accounts 연결 후에
            # article = article_form.save(commit=False)
            # article.user = request.user
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
    return render(request, 'articles:detail', context)

# @login_required
def update(request, articles_pk):
    article = get_object_or_404(Article, pk=articles_pk)
    # 로그인한 유저와 작성한 유저가 같다면
    # if request.user == article.user:
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
    # else:
    #     return redirect('articles:detail', articles_pk)
    
# @login_required
def delete(request, articles_pk):
    article = get_object_or_404(Article, pk=articles_pk)
    article.delete()
    return redirect('articles:index')

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

