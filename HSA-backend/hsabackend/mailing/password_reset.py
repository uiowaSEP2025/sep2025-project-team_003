from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
import os
from hsabackend.utils.env_utils import get_url

def send_password_reset(reset_token: str, username: str, email: str):
    link = f"{get_url()}/reset-password?token={reset_token}"

    context = Context({
        'username': username,
        'reset_link': link,
    })

    # Plain text email
    text_template = Template("""
        Hello {{ username }},

        You have requested to reset your password for HSA.

        If you did not request this change, please change your password.

        To reset your password, click the link below:
        {{ reset_link }}

        This link will expire in 30 minutes.
        """)

    # HTML email
    html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            .btn {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .container {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            </style>
        </head>
        <body>
            <div class="container">
            <h2>Hello {{ username }},</h2>
            <p>You have requested to reset your password for HSA.</p>
            <p>If you did not request this change, please change your password.</p>
            <p>To reset your password, click the button below:</p>
            <a href="{{ reset_link }}" class="btn">Reset Your Password</a>
            <p style="margin-top: 20px;">This link will expire in 30 minutes.</p>
            </div>
        </body>
        </html>
        """)

    subject = 'Password reset'
    from_email = os.environ.get('EMAIL_HOST_USER', None)
    to = [email]  # or dynamically passed in

    text_content = text_template.render(context)
    html_content = html_template.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
