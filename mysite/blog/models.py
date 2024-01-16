from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'  # черновик
        PUBLISHED = 'PB', 'Published'  # опубликовано

    title = models.CharField(max_length=250)  # название
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # уникальный slug исп. для поиска
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # пользователь
    body = models.TextField()  # текст
    publish = models.DateTimeField(default=timezone.now)  # дата публикации поста
    created = models.DateTimeField(auto_now_add=True)  # дата создания поста
    updated = models.DateTimeField(auto_now=True)  # дата обновления поста
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ['-publish']  # убывающий порядок по полю "publish"
        indexes = [
            models.Index(fields=['-publish']),
        ]  # извлечение данных по индексу

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
