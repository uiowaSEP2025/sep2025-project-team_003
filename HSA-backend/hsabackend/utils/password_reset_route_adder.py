""" URL Configuration for core auth """
from django.urls import path
from django_rest_passwordreset.views import reset_password_confirm, reset_password_request_token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.serializers import EmailSerializer, PasswordTokenSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import exceptions
from django_rest_passwordreset.views import clear_expired_tokens, generate_token_for_email
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, get_password_validators


app_name = 'password_reset'

HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')

class ResetPasswordConfirm(GenericAPIView):
    """
    An Api View which provides a method to reset a password based on a unique token
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = PasswordTokenSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        # change users password (if we got to this code it means that the user is_active)
        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(
                sender=self.__class__,
                user=reset_password_token.user,
                reset_password_token=reset_password_token,
            )
            try:
                # validate the password against existing validators
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                # raise a validation error for the serializer
                raise exceptions.ValidationError({
                    'password': e.messages
                })

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(
                sender=self.__class__,
                user=reset_password_token.user,
                reset_password_token=reset_password_token,
            )

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'OK'})
    
class ResetPasswordRequestToken(GenericAPIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        clear_expired_tokens()
        token = generate_token_for_email(
            email=serializer.validated_data['email'],
            user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
            ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
        )

        if token:
            # send a signal that the password token was created
            # let whoever receives this signal handle sending the email for the password reset
            reset_password_token_created.send(
                sender=self.__class__,
                instance=self, reset_password_token=token
            )

        return Response({'status': 'OK'})




class ResetPasswordConfirmViewSet(ResetPasswordConfirm, GenericViewSet):
    """
    An Api ViewSet which provides a method to reset a password based on a unique token
    """

    def create(self, request, *args, **kwargs):
        return super(ResetPasswordConfirmViewSet, self).post(request, *args, **kwargs)


class ResetPasswordRequestTokenViewSet(ResetPasswordRequestToken, GenericViewSet):
    """
    An Api ViewSet which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """

    def create(self, request, *args, **kwargs):
        return super(ResetPasswordRequestTokenViewSet, self).post(request, *args, **kwargs)



def add_reset_password_urls_to_router(router, base_path=''):
    router.register(
        base_path + "/confirm",
        ResetPasswordConfirmViewSet,
        basename='reset-password-confirm'
    )
    router.register(
        base_path,
        ResetPasswordRequestTokenViewSet,
        basename='reset-password-request'
    )


urlpatterns = [
    path("confirm/", reset_password_confirm, name="reset-password-confirm"),
    path("", reset_password_request_token, name="reset-password-request"),
]
