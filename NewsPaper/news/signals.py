from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper.news.models import PostCategory


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'news_create_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/.html')
    msg.send()


@receiver(post_save, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'news_create':
        categories = instance.postCategory.all()
        subscribers_email = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_email += [s.email for s in subscribers]

        send_notifications(instance.preview, instance.pk, instance.title, instance.subscribers)


