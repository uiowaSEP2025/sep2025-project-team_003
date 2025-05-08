from django.core.mail import EmailMultiAlternatives
from hsabackend.models.job import Job
import os
from hsabackend.utils.env_utils import get_url
from django.conf import settings
import jwt

def encode(job):
    return jwt.encode(job.jwt_json(), "vibecodedAPPS-willgetyouHACKED!!", algorithm="HS256")

def send_quotes_email(job: Job, pdf_bytes):
    def get_text(token):
            return (
                f"Hello {job.customer.first_name},\n\n"
                f"Please find attached the PDF quote for your requested job, and make a statement <a href={get_url() + f"/signquote?token={token}"}>here</a>.")

    # Prepare email
    subject = f"Quote for Job #{job.pk}"
    from_email = os.environ.get("EMAIL_HOST_USER")
    to_email = job.customer.email

    token = encode(job)

    text_content = get_text(token)
    html_content = f"""
        <p>Hello {job.customer.first_name},</p>
        <p>{text_content}</p>
        <p>If you have any questions, just hit reply.</p>
        <p>Best,<br/>HSA Team</p>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.attach(f"quote_job_{job.pk}.pdf", pdf_bytes, "application/pdf")
    msg.send()
    print(f"Sent a quote to customer with emailn {to_email[:4]}******")

    return to_email

def accept_reject_quotes(job: Job, decision: str):
    customer_email = job.customer.email
    from_email = os.environ.get("EMAIL_HOST_USER") or settings.DEFAULT_FROM_EMAIL

    if decision == "accept":
        job.quote_status = "accepted"
        subject = f"Quote #{job.pk} Approved"
        text = (
            f"Hello {job.customer.first_name},\n\n"
            f"Thank you! Your quote for Job #{job.pk} has been accepted.\n\n"
            "We’ll be in touch shortly to schedule the work.\n\n"
            "Best,\nHSA Team"
        )
    else:  
        job.quote_status = "rejected"
        job.quote_s3_link = None
        subject = f"Quote #{job.pk} Rejected"
        sign_url = f"{get_url()}/signquote?job_id={job.pk}"
        text = (
            f"Hello {job.customer.first_name},\n\n"
            f"Your quote for Job #{job.pk} was rejected.\n\n"
            f"If you’d like to make changes and sign again, please visit:\n{sign_url}\n\n"
            "Feel free to reach out with any questions.\n\n"
            "Best,\nHSA Team"
        )

    job.save(update_fields=["quote_status", "quote_s3_link"] if decision == "reject" else ["quote_status"])

    msg = EmailMultiAlternatives(subject, text, from_email, [customer_email])
    msg.send()