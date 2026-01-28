from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_order_confirmation(order_id, customer_email):
    # Here you can use your Order model to fetch details if needed
    subject = f"Order #{order_id} Confirmation"
    message = f"Your order {order_id} has been received. Thank you for shopping with us!"
    send_mail(subject, message, 'no-reply@myproject.com', [customer_email])
    return f"Confirmation sent for order {order_id}"
