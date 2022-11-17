from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from articles.models import Reservation


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect("articles:index")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("articles:index")
    
    if request.method == "POST":
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "articles:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("articles:index")


def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)

    context = {
        "user": user,
    }

    return render(request, "accounts/detail.html", context)


@login_required
def update(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", pk)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.delete()
    return redirect("articles:index")


# 비밀번호 변경
@login_required
def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # 로그인 유지
            return redirect("accounts:detail", request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/password.html", context)


def follow(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user != user and request.method == "POST":
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            is_followed = False
        else:
            user.followers.add(request.user)
            is_followed = True
        context = {
            "is_followed": is_followed,
        }
        return JsonResponse(context)
    return redirect("accounts:detail", user_pk)


@login_required
def block(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user != request.user:
        if user.blockers.filter(pk=request.user.pk).exists():
            user.blockers.remove(request.user)
            user.save()
        else:
            user.blockers.add(request.user)
            user.save()
    return redirect("accounts:detail", user.pk)


@login_required
def block_user(request):
    block_users = request.user.blocking.all()
    context = {
        "block_users": block_users,
    }
    return render(request, "accounts/block_user.html", context)


@login_required
def block_user_block(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user != request.user:
        if user.blockers.filter(pk=request.user.pk).exists():
            user.blockers.remove(request.user)
            user.save()
        else:
            user.blockers.add(request.user)
            user.save()
    return redirect("accounts:block_user")

def pay_history(request, user_pk):
    reservations = Reservation.objects.filter(user=user_pk)
    context = {
        'reservations':reservations,
        
    }
    return render(request, 'accounts/pay_history.html', context)