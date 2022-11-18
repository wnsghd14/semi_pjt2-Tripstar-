from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Theme(models.Model):
    title = models.CharField(max_length=20)
    image = ProcessedImageField(blank=True, upload_to='images/theme/', processors=[ResizeToFill(1600, 300)], format='JPEG', options={'quality':100})


class Region(models.Model):
    title = models.CharField(max_length=20)
    index_image = ProcessedImageField(blank=False, upload_to='images/region/', processors=[ResizeToFill(800, 600)], format='JPEG', options={'quality':100})
    detail_image = ProcessedImageField(blank=False, upload_to='images/region/', processors=[ResizeToFill(1600, 300)], format='JPEG', options={'quality':100})


class Article(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/articles/',null=True,
                                processors=[ResizeToFill(800, 600)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    theme = models.ManyToManyField(Theme, symmetrical=False, related_name='article_themes')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    
class Location(models.Model):
    location = models.CharField(max_length=300, blank=True)
    x = models.CharField(max_length=100, blank=True, null=True)
    y = models.CharField(max_length=100, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    

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
    image = ProcessedImageField(upload_to='images/reviews/',null=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 80})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    created_at = models.DateTimeField(auto_now_add=True)

class Age(models.IntegerChoices):
    zero = 0, '0'
    one = 1, '1'
    two = 2 , '2'
    three = 3 , '3'
    four = 4 , '4'
    five = 5 , '5'
    

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    adult = models.IntegerField(default=Age.zero, choices=Age.choices)
    kid = models.IntegerField(default=Age.zero, choices=Age.choices)
    date = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)