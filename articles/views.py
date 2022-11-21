from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Avg, Count
from django.contrib.auth import get_user_model
import json
import math
from collections import deque
from django.contrib import messages

# Create your views here.
def index(request):
    if request.session.get('recent_articles'):
        recent_articles = request.session.get('recent_articles')
    else:
        recent_articles = None
    context = {
        "articles": Article.objects.all().annotate(grade_avg=Avg('review__grade')),
        "regions": Region.objects.all(),
        "themes": Theme.objects.all(),
        'recent_articles': recent_articles,
        'best_articles': Article.objects.all().annotate(grade_avg=Avg('review__grade')).order_by('-grade_avg')[:3]
    }
    return render(request, "articles/index.html", context)


# 지역(region), 테마(theme)에 대해서 생성, 수정, 삭제할 수 있는 권한은 관리자(superuser)에게만 있음
def region_create(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = RegionForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('articles:theme_region_list')
        else:
            form = RegionForm()
        context = {
            'form':form
        }
        return render(request, 'articles/form.html', context)
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
        return redirect('articles:index')

def region_update(request, region_pk):
    region = get_object_or_404(Region, pk=region_pk)
    if request.user.is_superuser:
        if request.method == "POST":
            form = RegionForm(request.POST, request.FILES, instance=region)
            if form.is_valid():
                form.save()
                return redirect('articles:theme_region_list')
        else:
            form = RegionForm(instance=region)
        context = {
            'form':form,
        }
        return render(request, 'articles/form.html', context)
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
    return redirect('articles:index')

def region_delete(request, region_pk):
    region = get_object_or_404(Region, pk=region_pk)
    if request.user.is_superuser:
        if request.method == "POST":
            region.delete()
            return redirect('articles:theme_region_list')
        else:
            messages.warning(request, '잘못된 접근입니다.')
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
    return redirect('articles:index')

def theme_create(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = ThemeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('articles:theme_region_list')
        else:
            form = ThemeForm()
        context = {
            'form':form,
        }
        return render(request, 'articles/form.html', context)
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
        return redirect('articles:index')

def theme_update(request, theme_pk):
    theme = get_object_or_404(Theme, pk=theme_pk)
    if request.user.is_superuser:
        if request.method == "POST":
            form = ThemeForm(request.POST, request.FILES, instance=theme)
            if form.is_valid():
                form.save()
                return redirect('articles:theme_region_list')
        else:
            form = ThemeForm(instance=theme)
        context = {
            'form':form,
        }
        return render(request, 'articles/form.html', context)
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
        return redirect('articles:index')

def theme_delete(request, theme_pk):
    theme = get_object_or_404(Theme, pk=theme_pk)
    if request.user.is_superuser:
        if request.method == "POST":
            theme.delete()
            return redirect('articles:theme_region_list')
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
        return redirect('articles:index')
    

def theme_region_list(request):
    if request.user.is_superuser:
        context = {
            'regions':Region.objects.all(),
            'themes':Theme.objects.all(),
        }
        return render(request, 'articles/theme_region_list.html', context)
    else:
        messages.warning(request, '관리자만 접근가능합니다.')
        return redirect('articles:index')


@login_required
def create(request):
    locationform = LocationForm()
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        article_photo_form = ArticlePhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        locationform = LocationForm(request.POST)
        x = request.POST.getlist('x')
        y = request.POST.getlist('y')
        location = request.POST.getlist('location')
        
        if article_form.is_valid() and locationform.is_valid():
            # accounts 연결 후에
            article = article_form.save(commit=False)
            article.user = request.user
            location = locationform.save(commit=False)
            location.article = article

            article.region = get_object_or_404(Region, pk=request.POST.get("region"))

            if len(images):
                for image in images:
                    image_instance = ArticlePhoto(article=article, image=image)
                    article.save()
                    image_instance.save()
            location.save()
            article.save()

            for theme_pk in request.POST.getlist("theme"):
                theme = get_object_or_404(Theme, pk=theme_pk)
                article.theme.add(theme)
            messages.success(request, '성공적으로 등록되었습니다.')
            return redirect("articles:detail", article.pk)
    else:
        article_form = ArticleForm()
        article_photo_form = ArticlePhotoForm()
    context = {
        "article_form": article_form,
        "article_photo_form": article_photo_form,
        "regions": Region.objects.all(),
        "themes": Theme.objects.all(),
    }
    return render(request, "articles/create.html", context)


def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    reviews = Review.objects.filter(article=article)
    location = get_object_or_404(Location, article_id=article_pk)
    
    # 평균 별점
    grades = article.review.aggregate(grade_avg=Avg('grade'))
    quotient_list = []
    rest_list = []
    half_list = []
    if grades['grade_avg']:
        reviews_avg = grades['grade_avg']
        quotient = int(reviews_avg // 1)
        rest = round(reviews_avg % 1, 1)
        if 0.7 >= rest >= 0.3:
            half_list.append(1)
        elif rest > 0.7:
            quotient_list.append(1)
        for a in range(quotient):
            quotient_list.append(a)
        for a in range(5 - (len(quotient_list) + len(half_list))):
            rest_list.append(1)
    else:
        reviews_avg = 0
    
    # 각 별당 갯수
    grade_list = []
    total = article.review.all().count()
    if total:
      for cnt in range(5, 0, -1):
        grade_count = article.review.filter(grade=cnt).count()
        if grade_count:
          grade_list.append(round((grade_count / total) * 100))
        else:
          grade_list.append(0)

    article_photo = ArticlePhoto.objects.filter(article_id=article_pk)[0].image.url
    present_article = [article_pk, article_photo]
    if request.session.get('recent_articles'):
        recent_articles = request.session.get('recent_articles')
        if [article_pk, article_photo] in recent_articles:
            article_index = recent_articles.index(present_article)
            recent_articles.pop(article_index)
        if len(recent_articles) >= 4:
            recent_articles.pop()
        deq_recent_articles = deque(recent_articles)
        deq_recent_articles.appendleft([article_pk, article_photo])
        request.session['recent_articles'] = list(deq_recent_articles)
    else:
        request.session['recent_articles'] = [[article_pk, article_photo]]
    is_reserved = False
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(article=article)
        if reservations.filter(user=request.user).exists():
            is_reserved = True
    context = {
        "article": article,
        "reviews": reviews,
        "photo_cnt": article.articlephoto_set.count(),
        'location': location,
        'reviews_avg': reviews_avg,
        'quotient_list': quotient_list,
        'half_list': half_list,
        'rest_list': rest_list,
        'grade_list':grade_list,
        'is_reserved': is_reserved,
    }
    return render(request, "articles/detail.html", context)


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    photos = ArticlePhoto.objects.filter(article_id=article_pk)
    location = get_object_or_404(Location, article_id=article_pk)
    # 로그인한 유저와 작성한 유저가 같다면
    # if request.user == article.user:
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        article_photo_form = ArticlePhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        locationform = LocationForm(request.POST, instance=location)
        article.region = get_object_or_404(Region, pk=request.POST.get("region"))

        if article_form.is_valid() and article_photo_form.is_valid() and locationform.is_valid():
            article = article_form.save(commit=False)
            if len(images):
                for image in images:
                    image_instance = ArticlePhoto(article=article, image=image)
                    article.save()
                    image_instance.save()
            locationform.save()
            article.save()
            for existing_theme in article.theme.all():
                article.theme.remove(existing_theme)
            for theme_pk in request.POST.getlist("theme"):
                theme = get_object_or_404(Theme, pk=theme_pk)
                article.theme.add(theme)
            messages.success(request, '성공적으로 변경되었습니다.')
            return redirect("articles:detail", article_pk)
    else:
        article_form = ArticleForm(instance=article)
        article_photo_form = ArticlePhotoForm()
    context = {
        'article': article,
        'location': get_object_or_404(Location, article=article),
        "article_form": article_form,
        "article_photo_form": article_photo_form,
        "regions": Region.objects.all(),
        "themes": Theme.objects.all(),
    }
    return render(request, "articles/update.html", context)
    

# @login_required
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
            messages.success(request, '삭제되었습니다.')
    return redirect("articles:index")


@login_required
def like(request, pk):
    article = Article.objects.get(pk=pk)
    if article.like_users.filter(id=request.user.id).exists():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    context = {
        'isLiked': is_liked,
        'likeCount': article.like_users.count()
    }
    return JsonResponse(context)

def region_theme_articles(request, region_pk, theme_pk):
    region = get_object_or_404(Region, pk=region_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    context = {
        'region': region,
        'theme': theme,
        'articles': Article.objects.filter(Q(region=region) & Q(theme=theme))
    }
    return render(request, 'articles/region_theme_articles.html', context)

def region_theme_articles_grade(request, region_pk, theme_pk):
    region = get_object_or_404(Region, pk=region_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    articles = Article.objects.filter(Q(region=region) & Q(theme=theme)).annotate(grade_avg=Avg('review__grade'))
    context = {
        'region': region,
        'theme': theme,
        'articles': articles.order_by('-grade_avg')
    }
    return render(request, 'articles/region_theme_articles.html', context)

def region_theme_articles_review(request, region_pk, theme_pk):
    region = get_object_or_404(Region, pk=region_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    articles = Article.objects.filter(Q(region=region) & Q(theme=theme)).annotate(review_count=Count('review'))
    context = {
        'region': region,
        'theme': theme,
        'articles': articles.order_by('-review_count')
    }
    return render(request, 'articles/region_theme_articles.html', context)

def region_theme_articles_low(request, region_pk, theme_pk):
    region = get_object_or_404(Region, pk=region_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    context = {
        'region': region,
        'theme': theme,
        'articles': Article.objects.filter(Q(region=region) & Q(theme=theme)).order_by('price')
    }
    return render(request, 'articles/region_theme_articles.html', context)

def region_theme_articles_high(request, region_pk, theme_pk):
    region = get_object_or_404(Region, pk=region_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    context = {
        'region': region,
        'theme': theme,
        'articles': Article.objects.filter(Q(region=region) & Q(theme=theme)).order_by('-price')
    }
    return render(request, 'articles/region_theme_articles.html', context)

def region_theme_articles_recent(request, region_pk, theme_pk):
    region = get_object_or_404(Region, pk=region_pk)
    theme = get_object_or_404(Theme, pk=theme_pk)
    context = {
        'region': region,
        'theme': theme,
        'articles': Article.objects.filter(Q(region=region) & Q(theme=theme)).order_by('-created_at')
    }
    return render(request, 'articles/region_theme_articles.html', context)

def review_index(request):
    reviews = Review.objects.order_by("-pk")
    context = {
        "reviews": reviews,
    }
    return render(request, "articles/review_index.html", context)

@login_required
def review_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        review_photo_form = ReviewPhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            if len(images):
                for image in images:
                    image_instance = ReviewPhoto(review=review, image=image)
                    review.article = article
                    review.save()
                    image_instance.save()
            review.article = article
            review.save()
            messages.success(request, '성공적으로 등록되었습니다.')
            return redirect("articles:review_detail", review.pk)
    else:
        review_form = ReviewForm()
        review_photo_form = ReviewPhotoForm()
    context = {
        "review_form": review_form,
        "review_photo_form": review_photo_form,
    }
    return render(request, "articles/review_create.html", context)


def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": review.comment_set.all(),
        "photo_cnt": review.reviewphoto_set.count(),
    }
    return render(request, "articles/review_detail.html", context)

@login_required
def review_delete(request, review_pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        if request.user == review.user:
            review.delete()
            messages.success(request, '성공적으로 삭제되었습니다.')
            return redirect("articles:detail", review.article.pk)
    else:
        return redirect("articles:detail", review.article.pk)

@login_required
def review_update(request, review_pk):
    # article = Article.objects.get(pk=pk)
    review = Review.objects.get(pk=review_pk)
    photos = ReviewPhoto.objects.filter(review_id=review_pk)

    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        review_photo_form = ReviewPhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")

        if review_form.is_valid() and review_photo_form.is_valid():
            review = review_form.save(commit=False)
            if len(images):
                for image in images:
                    image_instance = ReviewPhoto(review=review, image=image)
                    review.save()
                    image_instance.save()
            review.save()
            messages.success(request, '성공적으로 변경되었습니다.')
            return redirect("articles:review_detail", review_pk)
    else:
        review_form = ReviewForm(instance=review)
        if photos:
            review_photo_form = ReviewPhotoForm(instance=photos[0])
        else:
            review_photo_form = ReviewPhotoForm()

    context = {
        "review_form": review_form,
        "review_photo_form": review_photo_form,
    }
    return render(request, "articles/review_create.html", context)

@login_required
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

@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("articles:review_detail", review_pk)

@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        if request.method == "POST":
            comment.delete()
            return redirect("articles:review_detail", review_pk)
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
        users = (
            get_user_model().objects.order_by("-pk").filter(username__contains=query)
        )
    context = {
        "query": query,
        "articles": articles,
        "reviews": reviews,
        "users": users,
    }
    return render(request, "articles/search.html", context)

def region_index(request, region_pk):
    region = get_object_or_404(Region, pk=region_pk)
    articles = region.article_set.all()
    regions = Region.objects.all()

    context = {
        'articles':articles,
        'region':region,
        'themes':Theme.objects.all(),
        'regions':regions,
    }
    return render(request, 'articles/region_index.html', context)

def theme_index(request, theme_pk):
    theme = get_object_or_404(Theme, pk=theme_pk)
    context = {
        'theme': theme,
        'articles': Article.objects.filter(theme=theme)
    }
    return render(request, 'articles/theme_index.html', context)

def map(request):
    return render(request, 'articles/map.html')

@login_required
def reservation_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST, request.FILES)
        if request.POST.get('name') == '':
            messages.warning(request, '이름을 입력해주세요')
            return redirect('articles:detail', article_pk)
        if request.POST.get('adult') == '0':
            messages.warning(request, '최소 인원은 1명입니다.')
            return redirect('articles:detail', article_pk)
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.user = request.user
            reservation.article = article
            reservation.save()
            return redirect("cart:kakaoPay", reservation.pk)
    # else:
    #     reservation_form = ReservationForm()
    # context = {
    #     "reservation_form": reservation_form,
    # }
    # return render(request, "articles/reservation_create.html", context)

def game(request):
    return render(request,'articles/game.html')