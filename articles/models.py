from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CategorySelect(models.IntegerChoices):
    one = 1, '경기도',
    two = 2, '강원도',
    three = 3, '제주도',
    four = 4, '경상도',
    five = 5, '전라도',
    six = 6, '충청도',
    seven = 7, '서울',
    eight = 8, '부산',
    nine = 9,'인천',
    ten = 10, '대전',
    eleven = 11, '대구',
    twelve = 12, '광주',


class Article(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    content = models.TextField()
    category = models.IntegerField(default=CategorySelect.seven, choices=CategorySelect.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/',null=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='article_like')


class GradeSelector(models.IntegerChoices):
    one = 1, '⭐'
    two = 2, '⭐⭐'
    three = 3, '⭐⭐⭐'
    four = 4, '⭐⭐⭐⭐'
    five = 5, '⭐⭐⭐⭐⭐'


class Review(models.Model):
    articles = models.ForeignKey(Article,on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = ProcessedImageField(upload_to='images/',null=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 80})
    created_at = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(auto_now=True),
    grade = models.IntegerField(default=GradeSelector.five,choices=GradeSelector.choices)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='review_like')


class Comment(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()