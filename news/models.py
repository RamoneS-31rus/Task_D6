from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True)
    rating = models.IntegerField(default=0)

    def update_rating(self, rating):
        self.rating = rating
        value_post = Author.objects.filter(Post.post_rating)  # каждой статьи автора
        value_author = Author.objects.filter(Comment.comment_rating)  # всех комментариев автора
        value_comment = Author.objects.filter(Post.post_rating, Comment.comment_rating)  # всех комментариев к статьям автора
        value = value_post * 3 + value_author + value_comment
        self.rating = value
        self.save()

    def __str__(self):
        return '%s' % self.author

class Category(models.Model):
    title = models.CharField(unique=True, max_length=120)

    def __str__(self):
        return self.title


class Post(models.Model):
    news = 'Новость'
    article = 'Статья'
    type = [(news, 'Новость'), (article, 'Статья')]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE) # Автор
    post_type = models.CharField(max_length=30, choices=type, default=news) # Тип публикации
    post_time = models.DateTimeField(auto_now_add=True) # Дата создания
    post_category = models.ManyToManyField(Category) # Категории
    post_title = models.CharField(max_length=50) # Заголовок
    post_text = models.TextField() # Текст
    post_rating = models.IntegerField(default=0) # Рейтинг
    post_likes = models.IntegerField(default=0) # Понравилось
    post_dislikes = models.IntegerField(default=0) # Не понравилось

    def __str__(self):
        return self.post_title

    def preview(self):
        return self.post_text[:124] + '...'

    def like(self):
        self.post_likes += 1
        self.post_rating = self.post_likes
        self.save()

    def dislike(self):
        self.post_dislikes += 1
        self.post_rating = self.post_likes - self.post_dislikes
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE) # Комментарии пользователя
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE) # Комментарии к публикации
    comment_text = models.TextField() # Текст комментария
    comment_time = models.DateTimeField(auto_now_add=True) # Дата создания
    comment_rating = models.IntegerField(default=0) # Рейтинг
    comment_likes = models.IntegerField(default=0) # Понравилось
    comment_dislikes = models.IntegerField(default=0) # Не понравилось

    def __str__(self):
        return self.comment_text

    def like(self):
        self.comment_likes += 1
        self.comment_rating = self.comment_likes
        self.save()

    def dislike(self):
        self.comment_dislikes += 1
        self.comment_rating = self.comment_likes - self.comment_dislikes
        self.save()

