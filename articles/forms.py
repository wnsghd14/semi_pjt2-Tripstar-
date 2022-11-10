from .models import Article, Comment, Review
from django import forms

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
            "image",
        ]
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

