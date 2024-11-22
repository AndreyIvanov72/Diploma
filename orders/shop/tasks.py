from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_email(email):
    send_mail(
        "Поздравляю! Вы успешно зарегистрировались!",
        "Регистрация прошла успешно, удачных покупок!",
        "pivorc72@mail.ru",
        [email],
        fail_silently=False,
    )

@shared_task
def send_contact_confirmation_email(email):
    send_mail(
        "Подтверждение адреса",
        "Адрес успешно добавлен",
        "pivorc72@mail.ru",
        [email],
        fail_silently=False,
    )

@shared_task
def send_order_confirmation_email(email):
    send_mail(
        "Заказ подтвержден",
        "Поздравляем с покупкой!",
        "pivorc72@mail.ru",
        [email],
        fail_silently=False,
    )