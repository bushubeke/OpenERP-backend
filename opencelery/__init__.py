from celery import Celery
from fastapi_mail import FastMail, ConnectionConfig
from config import settings, celeryconf

# https://www.cherryservers.com/blog/how-to-install-and-start-using-rabbitmq-on-ubuntu-22-04
# https://testdriven.io/blog/fastapi-and-celery/
## celery -A opencelery.core flower worker --loglevel=info -Q opencelery
# celery -A opencelery.app  worker -l INFO --logfile=celerylog/log
# ./rabbitmqadmin --username=bushu --password=yahweh --vhost='openerp' delete queue name='opencelery'
# celery -A opencelery.app  worker --concurrency=2 -l INFO --logfile=celerylog/log
# sudo mkdir /var/log/celery
# sudo chown -R bushu:bushu /var/log/celery
# sudo chmod o+w /var/run/celery
# sudo chmod o+w /var/log/celery
settings = settings.dict()


mail_conf = ConnectionConfig(
    MAIL_SERVER='smtp.aol.com',
    MAIL_USERNAME=settings['MAIL_USERNAME'],
    MAIL_PASSWORD=settings['MAIL_PASSWORD'],
    MAIL_FROM=settings['MAIL_DEFAULT_SENDER'],
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
def create_celery():
    celery_app = Celery("OPENERP BROKER", include=['opencelery.core'])
    celery_app.config_from_object(celeryconf,namespace="CELERY")
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_serializer='pickle')
    celery_app.conf.update(result_serializer='pickle')
    celery_app.conf.update(accept_content=['pickle', 'json'])
    celery_app.conf.update(result_expires=200)
    celery_app.conf.update(result_persistent=True)
    celery_app.conf.update(worker_send_task_events=True)
    celery_app.conf.update(worker_prefetch_multiplier=1)
    celery_app.conf.update(task_create_missing_queues=True)

    #
    # celery_app.conf.update(
    #     security_key='ssl.key',
    #     security_certificate = 'ssl.cert',
    #     security_cert_store = '/*.cert',
    #     security_digest = 'sha256',
    #     task_serializer = 'auth',
    #     event_serializer = 'auth',
    #     accept_content = ['auth']
    # )

    return celery_app
argv = [
    'worker',
    '-l=DEBUG',
    '-P',
    'eventlet',
    '-c=100',
    '--without-gossip',
    '--without-mingle',
    '--without-heartbeat',
    '-Ofair',
]
app = create_celery()
mail = FastMail(mail_conf)
