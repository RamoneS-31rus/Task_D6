from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def notify_singup(sender, created, **kwargs):

    user = User.objects.order_by('-id')[0]
    mail = [user.email]

    msg = EmailMultiAlternatives(
        subject=f'Регистрация',
        body=f'Вы зарегистрировались на сайте.',
        from_email='ramones.31rus@yandex.com',
        to=mail,
    )

    msg.send()

