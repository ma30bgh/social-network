from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    #related_name baraye ertebat bar axe yani chi?
    #baraye ertebate barax ma inja az tarighe p1 = Post.objects.first()  -->  p1.user
    #vali az user b post dastresi nadarim (mitonim az __set estefade konim k khob nis)
    #p1 = User.objects.first()  --> p1.posts.all()
    #havaset bashe related_name ro esmi entekhab koni k eyn esm classet nabashe
    body = models.TextField(max_length=500)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', 'body']
        #in ja darim tartib namayesh ro moshakhas mikonim
        #chera 2 ta fild neveshtim? k age avali yeksan bod bar asas dovomi bashe
        #age faghad ye shart dashtim az () estefade mikonim --> ('body',)

#in tabe behet komak mikone ke to panel admin mikhay post ha che jori namayesh dade beshan
    def __str__(self):
        return f'{self.slug} - {self.updated}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def likes_count(self):
        return self.pvotes.count()

    def user_can_like(self,user):
        user_like=user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    #self eshare mikone b hamin class
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.user} Liked {self.post.slug}'