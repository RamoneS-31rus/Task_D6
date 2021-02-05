from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from news.models import Post, Category
from django.core.management.base import BaseCommand
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

def my_job():
    week = localtime() - timedelta(days=7)
    categories = Category.objects.all()
    email_subscribers = []

    for category in categories:
        subscribers = Category.objects.get(title=category).subscribers.all()
        for user in subscribers:
            email_subscribers.append(user.email)

            posts = Post.objects.filter(post_category__title=category, post_time__gt=week)
            content = render_to_string('news/newsletter.html',
                                       {'posts': posts,
                                        'category': category,
                                        }
                                       )

            msg = EmailMultiAlternatives(
                subject=f'Новости за неделю',
                from_email='info.django@yandex.ru',
                to=email_subscribers,
                )
            msg.attach_alternative(content, "text/html")
            msg.send()
            print('Hello!')


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

