from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
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
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def update(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", pk)
    else:
        form = CustomUserCreationForm(instance=user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.delete()
    return redirect("articles:index")
