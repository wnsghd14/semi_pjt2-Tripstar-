from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        help_text='',
    )
    password1 = forms.CharField(
        help_text='',
    )
    password2 = forms.CharField(
        help_text='',
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "is_seller", "email", "password1", "password2"]
        labels = {
            'username': 'ID',
            'email': '이메일',
            'is_seller': 'Seller 계정',
            'image': '프로필 사진',
        }

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "content", "image", 'is_seller']
        labels = {
            'username': 'ID',
            'email': '이메일',
            'content': '소개',
            'image': '프로필 사진',
        }