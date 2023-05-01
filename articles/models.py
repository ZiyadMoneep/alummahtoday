import time
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.urls import reverse

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    img = models.ImageField(blank=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
                on_delete=models.SET(get_sentinel_user),
    )

    def __str__(self):
        return f"{self.title} -- {self.date} -- {self.author}"

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[str(self.id)])


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=160)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.comment} -- {self.author}"

    def get_absolute_url(self):
        return reverse("articles:article_list")
