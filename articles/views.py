from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article
from django.contrib.auth.decorators import login_required
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