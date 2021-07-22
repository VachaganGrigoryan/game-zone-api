from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_multi_format_email(template_prefix, template_context, target_email):
    subject_file = f'account/{template_prefix}_subject.txt'
    text_file = f'account/{template_prefix}.txt'
    html_file = f'account/{template_prefix}.html'

    from_email = settings.EMAIL_FROM
    bcc_email = settings.EMAIL_BCC
    subject = render_to_string(subject_file).strip()
    text_content = render_to_string(text_file, template_context)
    html_content = render_to_string(html_file, template_context)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [target_email],
        bcc=[bcc_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
