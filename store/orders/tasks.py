from store.celery import app
from django.core.mail import send_mail
from .models import Order


@app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject=f'Заказ №{order_id}'
    message = f'Уважаемый {order.first_name, order.last_name}, заказ находится в обработке.'

    mail_sent = send_mail(subject=subject,
                           message=message,
                           from_email='admin@store.com',
                            recipient_list=[order.email])
    return mail_sent


