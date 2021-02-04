from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category, PostCategory
from django.contrib.auth.models import User


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_post(sender, instance, **kwargs):
    changed_category = Post.objects.order_by('-id')[0].post_category.all()
    email_subscribers = []

    for tag in changed_category:
        for i in range(len(Category.objects.get(title=tag).subscribers.all())):
            email_subscribers.append(Category.objects.get(title=tag).subscribers.all()[i].email)

    link_id = instance.id
    post_title = f'{instance.post_title}'
    post_text = f'{instance.post_text}'
    link = f'http://127.0.0.1:8000/news/{link_id}'

    msg = EmailMultiAlternatives(
        subject='Появились обновления в категории на которую вы подписаны',
        from_email='ramones.31rus@yandex.ru',
        to= email_subscribers
    )

    html_content = render_to_string('/news/create_email.html',
                                    {'post_title': post_title,
                                     'post_text': post_text,
                                     'link': link,
                                     }
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
