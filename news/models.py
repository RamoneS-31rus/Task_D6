from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rat_author = self.author
        rat_post = 0
        rat_com = 0
        rat_post_com = 0
        for i in range(len(Post.objects.filter(post_author=Author.objects.get(author=User.objects.get(username=rat_author))))):
            rat_post += Post.objects.filter(post_author=Author.objects.get(author=User.objects.get(username=rat_author)))[i].post_rating

        for i in range(len(Comment.objects.filter(comment_user=User.objects.get(username=rat_author)))):
            rat_com += Comment.objects.filter(comment_user=User.objects.get(username=rat_author))[i].comment_rating

        for post in Post.objects.filter(post_author=Author.objects.get(author=User.objects.get(username=rat_author))):
            for i in range(len(Comment.objects.filter(comment_post=Post.objects.get(post_title=post)))):
                rat_post_com += Comment.objects.filter(comment_post=Post.objects.get(post_title=post))[i].comment_rating

        rat_sum = rat_post * 3 + rat_com + rat_post_com
        self.rating = rat_sum
        self.save()

    def __str__(self):
        return f'{self.author}'

class Category(models.Model):
    title = models.CharField(unique=True, max_length=120)

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    news = 'Новость'
    article = 'Статья'
    type = [(news, 'Новость'), (article, 'Статья'), ('select', 'Выбрать')]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор') # Автор
    post_type = models.CharField(max_length=30, choices=type, default='select', verbose_name='Тип') # Тип публикации
    post_time = models.DateTimeField(auto_now_add=True) # Дата создания
    post_category = models.ManyToManyField(Category, verbose_name='Категории') # Категории
    post_title = models.CharField(max_length=50, verbose_name='Заголовок') # Заголовок
    post_text = models.TextField(verbose_name='Текст') # Текст
    post_rating = models.IntegerField(default=0) # Рейтинг
    post_likes = models.IntegerField(default=0) # Понравилось
    post_dislikes = models.IntegerField(default=0) # Не понравилось

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.id}'

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

    def __str__(self):
        return f'{self.post_title}'


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

    def like(self):
        self.comment_likes += 1
        self.comment_rating = self.comment_likes
        self.save()

    def dislike(self):
        self.comment_dislikes += 1
        self.comment_rating = self.comment_likes - self.comment_dislikes
        self.save()

    def __str__(self):
        return f'{self.comment_text}'