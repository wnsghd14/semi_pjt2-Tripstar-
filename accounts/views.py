from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth  import get_user_model
from django.http import JsonResponse
# Create your views here.

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
            'is_followed': is_followed,
        }
        return JsonResponse(context)
    return redirect('accounts:detail', user_pk)