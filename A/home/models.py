from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

#in tabe behet komak mikone ke to panel admin mikhay post ha che jori namayesh dade beshan
    def __str__(self):
        return f'{self.slug} - {self.updated}'