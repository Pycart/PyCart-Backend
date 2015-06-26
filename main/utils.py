from django.core.mail import EmailMessage
from django.template import Context, loader
from project.settings import EMAIL_HOST_USER


def send_order_confirmation(first_name, email, order):
    """
    """
    template = loader.get_template("email_template.html")
    context = Context({"first_name": first_name, 'order': order})
    message = template.render(context)

    subject = "Thank you for submitting the form."
    from_emails = EMAIL_HOST_USER
    msg = EmailMessage(subject, message, from_emails, [email])
    msg.content_subtype = "html"
    msg.send()