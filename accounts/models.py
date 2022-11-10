from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=100)
    image = ProcessedImageField(upload_to='images/',null=True,
                                processors=[ResizeToFill(200, 100)],
                                format='JPEG',
                                options={'quality': 80})
    content = models.TextField()
    is_seller = models.BooleanField(default=False)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')