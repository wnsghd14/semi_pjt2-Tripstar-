from django.db import models
from articles.models import Reservation, Article
from accounts.models import User
# Create your models here.

class Pay(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    