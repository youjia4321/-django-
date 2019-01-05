from user.models import EmailCodeRecord
from random import Random
from blogs.settings import EMAIL_FROM
from django.core.mail import send_mail


def random_str(random_length=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_email_register(email, send_type="register"):
    email_record = EmailCodeRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    
    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活你的帐号： http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "重置密码链接"
        email_body = "请点击下面的重置你的密码： http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass