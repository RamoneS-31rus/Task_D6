from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category


@receiver(m2m_changed, sender=Post.post_category.through)
def notify_post(sender, instance, **kwargs):
    print("test")

    changed_category = Post.objects.order_by('-id')[0].post_category.all()
    email_subscribers = []

    for tag in changed_category:
        for i in range(len(Category.objects.get(title=tag).subscribers.all())):
            email_subscribers.append(Category.objects.get(title=tag).subscribers.all()[i].email)

    category = ''
    for i in changed_category:
        category += (i.title + ' ')

    text = f'{instance.post_text}'
    title = f'{instance.post_title}'

    url_id = instance.id
    url = f'http://127.0.0.1:8000/news/{url_id}'
    content = render_to_string('news/post_email.html', {'category': category,
                                                          'title': title,
                                                          'text': text,
                                                          'url': url,
                                                          }
                               )

    msg = EmailMultiAlternatives(
        subject=f'Появились обновления в категории на которую вы подписаны',
        from_email='info.django@yandex.ru',
        to=email_subscribers,
    )
    msg.attach_alternative(content, "text/html")
    msg.send()