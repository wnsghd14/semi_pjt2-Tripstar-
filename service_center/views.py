from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceCenterForm, CommentForm
from .models import ServiceCenter, ServiceComment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'service_center/index.html')

@login_required
def question(request):
    if request.method == "POST":
        service_form = ServiceCenterForm(request.POST,request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect(request.GET.get("next") or 'service_center:my_question')
    else:
        service_form = ServiceCenterForm()
    context = {
        'service_form':service_form,
    }
            
    return render(request, 'service_center/question.html', context)

@login_required
def detail(request, service_pk):
    question = ServiceCenter.objects.get(pk=service_pk)
    if request.user == question.user or request.user.is_superuser:
        comment_form = CommentForm()
        context = {
            'question':question,
            'comment_form':comment_form,
            'comments':question.center.all(),
        }
        return render(request, 'service_center/detail.html', context)
    else:
        messages.warning(request, '작성자만 접근할 수 있습니다.')
        return redirect('service_center:index') 

@login_required
def create_comment(request, service_pk):
    question = get_object_or_404(ServiceCenter, pk=service_pk)
    if request.user.is_superuser:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.service = question
            comment.user = question.user
            comment.save()
        return redirect('service_center:detail', question.pk)
    
@login_required
def update(request, service_pk):
    question = get_object_or_404(ServiceCenter, pk=service_pk)
    if request.user == question.user:
        if request.method == "POST":
            service_form = ServiceCenterForm(request.POST, request.FILES, instance=question)
            if service_form.is_valid():
                service_form.save()
                return redirect('service_center:detail', question.pk)
        else:
            service_form = ServiceCenterForm(instance=question)
        context = {
            'service_form':service_form,
        }
        return render(request, 'service_center/update.html', context)
    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('service_center:detail', question.pk)


def admin_page(request):
    questions = ServiceCenter.objects.order_by('-pk')
    if request.user.is_superuser:
        context = {
            'questions':questions,
        }
        return render(request, 'service_center/admin_page.html', context)
    else:
        return redirect('service_center:index')

def delete_comment(request,service_pk, question_pk):
    if request.user.is_superuser:
        comment_delete = ServiceComment.objects.get(pk=service_pk)
        comment_delete.delete()
    return redirect('service_center:detail', question_pk)

def my_question(request):
    return render(request, 'service_center/my_question.html')