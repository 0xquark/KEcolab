from celery import Celery

celery = Celery(__name__)
celery.config_from_object('celeryconfig')

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
