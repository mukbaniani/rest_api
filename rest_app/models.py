from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='კატეგორია')

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='სათაური')
    short_desc = models.TextField(verbose_name='მოკლე აღწერა')
    desc = models.TextField(verbose_name='აღწერა')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='კატეგორია')

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='კომენტარი')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='პოსტრის კომენტარი')

    def __str__(self):
        return self.comment

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)