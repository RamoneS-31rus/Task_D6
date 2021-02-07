from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)  # отправляем новомому пользователю уведомление на почту, после регистрации
def notify_singup(sender, created, **kwargs):

    user = User.objects.order_by('-id')[0]
    mail = [user.email]

    msg = EmailMultiAlternatives(
        subject=f'Регистрация',
        body=f'Спасибо, что Вы зарегистрировались на нашем сайте.',
        from_email='info.django@yandex.com',
        to=mail,
    )

    msg.send()


@receiver(post_save, sender=User)  # добавляем нового пользователя в группу 'common'
def save(sender, created, **kwargs):
    user = User.objects.order_by('-id')[0]
    basic_group = Group.objects.get(name='common')
    basic_group.user_set.add(user)
    return user

