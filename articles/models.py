from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Theme(models.Model):
    title = models.CharField(max_length=20)
    image = ProcessedImageField(blank=True, upload_to='images/', processors=[Thumbnail(200, 100)], format='JPEG', options={'quality':90})

class Region(models.Model):
    title = models.CharField(max_length=20)
    index_image = ProcessedImageField(blank=False, upload_to='images/', processors=[ResizeToFill(400, 300)], format='JPEG', options={'quality':90})
    detail_image = ProcessedImageField(blank=False, upload_to='images/', processors=[ResizeToFill(400, 100)], format='JPEG', options={'quality':90})

class Article(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/',null=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    theme = models.ManyToManyField(Theme, symmetrical=False, related_name='article_themes')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class ArticlePhoto(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/articles", blank=True, null=True)


class GradeSelector(models.IntegerChoices):
    one = 1, '⭐'
    two = 2, '⭐⭐'
    three = 3, '⭐⭐⭐'
    four = 4, '⭐⭐⭐⭐'
    five = 5, '⭐⭐⭐⭐⭐'


class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = ProcessedImageField(upload_to='images/',null=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 80})
    created_at = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(auto_now=True),
    grade = models.IntegerField(default=GradeSelector.five,choices=GradeSelector.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='review')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='review_like')


class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/reviews", blank=True, null=True)


class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)