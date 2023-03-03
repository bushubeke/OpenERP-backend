from . import mail
from celery import shared_task
from fastapi_mail import MessageSchema, MessageType


@shared_task(name="send_celery_email", bind=True)
def send_celery_email(self,value, email):
        html = f"""<p>Thanks for using Fastapi-mail {value}</p>"""
        message = MessageSchema(
                        subject="OpenERP-Mail module",
                        recipients=email,
                        body=html,
                        subtype=MessageType.html)
        print(message.dict())
        from asyncio import get_event_loop
        get_event_loop().run_until_complete(mail.send_message(message))
        return "Works Exccelent"


@shared_task(name="reverse", bind=True)
def reverse(self,myname):
    return myname[::-1]
