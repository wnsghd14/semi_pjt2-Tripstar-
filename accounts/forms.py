from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "is_seller", "email", "image"]
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
        fields = ["username", "email", "content", "image"]
        labels = {
            'username': 'ID',
            'email': '이메일',
            'content': '소개',
            'image': '프로필 사진',
        }