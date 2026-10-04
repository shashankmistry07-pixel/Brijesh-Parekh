import logging
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def _send_email_safe(subject, text_content, html_content, to_email, reply_to=None):
    """
    Helper to send a multi-part (HTML + Plain Text) email safely.
    """
    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Brijesh Parekh Official <brijesh71090parekh@gmail.com>')
        headers = {}
        if reply_to:
            headers['Reply-To'] = reply_to

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email] if isinstance(to_email, str) else to_email,
            headers=headers
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"Email successfully sent to {to_email} with subject: '{subject}'")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}", exc_info=True)
        return False


def send_admin_inquiry_notification(inquiry):
    """
    Sends an email notification to Brijesh Parekh's management team for each new booking inquiry.
    """
    admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'brijesh71090parekh@gmail.com')
    subject = f"✦ New Booking Inquiry: {inquiry.name} - {inquiry.event_type}"
    
    context = {'inquiry': inquiry}
    
    try:
        html_content = render_to_string('emails/admin_inquiry_notification.html', context)
    except Exception:
        html_content = f"<p>New inquiry from {inquiry.name} ({inquiry.email}, {inquiry.phone}) for {inquiry.event_type}:<br>{inquiry.message}</p>"
        
    try:
        text_content = render_to_string('emails/admin_inquiry_notification.txt', context)
    except Exception:
        text_content = f"New inquiry from {inquiry.name} ({inquiry.email}, {inquiry.phone}) for {inquiry.event_type}:\n{inquiry.message}"

    return _send_email_safe(
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        to_email=admin_email,
        reply_to=inquiry.email
    )


def send_client_inquiry_confirmation(inquiry):
    """
    Sends an automated professional acknowledgement & confirmation email to the client.
    """
    if not inquiry.email:
        return False

    subject = f"Thank you for contacting Brijesh Parekh | Booking Inquiry Received"
    context = {'inquiry': inquiry}

    try:
        html_content = render_to_string('emails/client_inquiry_confirmation.html', context)
    except Exception:
        html_content = f"<p>Dear {inquiry.name},<br>Thank you for contacting Brijesh Parekh's team. We will get back to you shortly.</p>"

    try:
        text_content = render_to_string('emails/client_inquiry_confirmation.txt', context)
    except Exception:
        text_content = f"Dear {inquiry.name},\nThank you for contacting Brijesh Parekh's team. We will get back to you shortly."

    return _send_email_safe(
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        to_email=inquiry.email
    )


def _dispatch_inquiry_emails(inquiry):
    """
    Executes both admin notification and client confirmation.
    """
    send_admin_inquiry_notification(inquiry)
    send_client_inquiry_confirmation(inquiry)


def send_inquiry_emails(inquiry, async_send=True):
    """
    Dispatches both inquiry emails. If async_send is True, launches in a background thread
    so the web UI responds instantly without any delay.
    """
    if async_send:
        t = threading.Thread(target=_dispatch_inquiry_emails, args=(inquiry,), daemon=True)
        t.start()
        return t
    else:
        _dispatch_inquiry_emails(inquiry)
        return True
