from .models import *
from django import forms
from django.forms import ClearableFileInput

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'price',
            'content',
            'category',
            'image',
        )
        labels = {
            'title': '제목',
            'price': '가격',
            'content': '내용',
            'category' : '카테고리',
            'image' : '이미지 업로드',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "grade",
        ]
        

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image",)
        widgets = {
            "image": ClearableFileInput(attrs={"multiple": True}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

