from .models import ServiceCenter, ServiceComment
from django import forms

class ServiceCenterForm(forms.ModelForm):
    class Meta:
        model = ServiceCenter
        fields = (
            'title',
            'content',
            'image',
        )
        labels = {
            'title': '문의 제목',
            'content': '문의 내용',
            'image': '이미지 업로드',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = ServiceComment
        fields = ('content',)
        labels = {
            'content': '답변',
        }