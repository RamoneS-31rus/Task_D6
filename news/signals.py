from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from django.contrib.auth.models import User


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.post_category.through)
def notify_post(sender, **kwargs):
    print("test")

    changed_category = Post.objects.order_by('-id')[0].post_category.all()
    email_subscribers = []

    for tag in changed_category:
        for i in range(len(Category.objects.get(title=tag).subscribers.all())):
            email_subscribers.append(Category.objects.get(title=tag).subscribers.all()[i].email)


    msg = EmailMultiAlternatives(
        body=f'Появились обновления в категории на которую вы подписаны',
        from_email='ramones.31rus@yandex.ru',
        to=email_subscribers,
    )

    msg.send()
