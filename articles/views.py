from django.http import JsonResponse,HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from .models import Review,Comment
from .forms import CommentForm
# Create your views here.
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