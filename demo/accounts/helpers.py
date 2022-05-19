import re
from django.conf import settings
from django.core.mail import send_mail
import threading
from django.template.loader import render_to_string


def email_validation_check(email):
    """
    for email, valid syntax returns True, else False.
    :param email:
    :return:
    """
    regex = "^[a-z0-9A-Z]+[\._]?[a-z0-9A-Z]+[@]\w+-?\w+[.]\w{2,3}$"
    if re.search(regex, email):
        return True
    else:
        return False


def check_if_password_match(password, repassword):
    if password == repassword:
        return True
    else:
        return False


class EmailThread(threading.Thread):
    def __init__(self, subject, to_email_list, template_name, template_content):
        self.subject = subject
        self.to_email_list = to_email_list
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.template_name = template_name
        self.html_body = render_to_string(template_name, context=template_content)
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            "",
            self.from_email,
            self.to_email_list,
            html_message=self.html_body,
        )


def send_html_mail(subject, to_email_list, template_name, template_content):
    EmailThread(subject, to_email_list, template_name, template_content).start()


class EmailThreadPlain(threading.Thread):
    def __init__(self, subject, message, to_email_list):
        self.subject = subject
        self.message = message
        self.to_email_list = to_email_list
        self.from_email = settings.DEFAULT_FROM_EMAIL
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.to_email_list)


def send_plain_mail(subject, message, to_email_list):
    EmailThreadPlain(subject, message, to_email_list).start()

