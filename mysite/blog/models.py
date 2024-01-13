from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Создание модели


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'  # черновик
        PUBLISHED = 'PB', 'Published'  # опубликовано

    title = models.CharField(max_length=250)  # название
    slug = models.SlugField(max_length=250)  # slug исп. для поиска
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')  # пользователь
    body = models.TextField()  # текст
    publish = models.DateTimeField(default=timezone.now)  # дата публикации поста
    created = models.DateTimeField(auto_now_add=True)  # дата создания поста
    updated = models.DateTimeField(auto_now=True)  # дата обновления поста
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']  # убывающий порядок по полю "publish"
        indexes = [
            models.Index(fields=['-publish']),
        ]  # извлечение данных по индексу

    def __str__(self):
        return self.title
