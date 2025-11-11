import mailtrap as mt
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

def send_invitation_email(invitation, request):
    """
    Sends a styled HTML invitation email using Mailtrap API.
    """
    # Build the accept URL
    accept_url = f"{request.scheme}://{request.get_host()}/api/auth/accept-invite/?token={invitation.token}"

    # Prepare context for the email template
    context = {
        "email": invitation.email,
        "role": invitation.get_role_display(),
        "accept_url": accept_url,
        "expires_at": invitation.expires_at,
        "now": timezone.now(),
    }

    # Render HTML template
    html_content = render_to_string("invite.html", context)

    # Build the Mailtrap email
    mail = mt.Mail(
        sender=mt.Address(email="admin@expressmartke.com", name="Expressmart Admin"),
        to=[mt.Address(email=invitation.email)],
        subject="You're invited to join The Expressmart Dashboard",
        html=html_content,
        category="User Invitation",
    )

    # Send via Mailtrap client
    client = mt.MailtrapClient(token=settings.MAILTRAP_API_TOKEN)
    response = client.send(mail)
    return response

def send_admin_password_reset_request_email(admin_emails, user):
    """
    Sends an email to all admins notifying them that a user requested a password reset.
    """
    context = {
        "user": user,
        "requested_at": timezone.now(),
    }
    html_content = render_to_string("reset_request.html", context)

    mail = mt.Mail(
        sender=mt.Address(email="admin@expressmartke.com", name="Expressmart Admin"),
        to=[mt.Address(email=email) for email in admin_emails],
        subject=f"Password Reset Request from {user.email}",
        html=html_content,
        category="Password Reset Request",
    )

    client = mt.MailtrapClient(token=settings.MAILTRAP_API_TOKEN)
    response = client.send(mail)
    return response


def send_password_reset_email(user, reset_url, expires_at):
    """
    Sends a styled password reset email using Mailtrap's Live mode.
    """

    context = {
        "user": user,
        "reset_url": reset_url,
        "expires_at": expires_at,
        "now": timezone.now(),
    }

    html_content = render_to_string("password_reset.html", context)

    mail = mt.Mail(
        sender=mt.Address(email="admin@expressmartke.com", name="Expressmart Admin"),
        to=[mt.Address(email=user.email)],
        subject="Password Reset Request Approved",
        html=html_content,
        category="Password Reset",
    )

    client = mt.MailtrapClient(token=settings.MAILTRAP_API_TOKEN)
    response = client.send(mail)
    return response