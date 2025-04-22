
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from hsabackend.mailing.password_reset import send_password_reset

@receiver(reset_password_token_created)
def handle_reset_password_token_created(sender, instance, reset_password_token, **kwargs):
    reset_token = reset_password_token.key
    username = reset_password_token.user.username
    email = reset_password_token.user.email

    send_password_reset(reset_token=reset_token, username=username, email=email)