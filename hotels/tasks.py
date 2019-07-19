from celery.decorators import task
from main.celery import app
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from .models import Reservation


@app.task(name='send_notification')
def send_notification():
    present = datetime.now()
    reservations = Reservation.objects.filter(expired_at__contains=present.strftime('%Y-%m-%d'))
    # users_emails = []
    if reservations.count() > 0:
        for r in reservations:
            print(f'deleting reservation --- {1}',format(r))
            # users_emails.insert(0, r.user.email)
            room = r.room
            r.delete()
            room.is_avaliable = True
            room.save()
            subject = 'Reservation Expired'
            from_mail = 'aa6653312@gmail.com'
            to_mail = [r.user.email,]
            context = {
                'name': r.user.username,
                'expire_date': 'date',
            }
            message = get_template('mesages/delete-notification-template.html').render(context)

            msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
            msg.attach_alternative(message, "text/html")
            msg.send()
        print('sending emails done')
    else:
        print('No Emails To be Sent')
