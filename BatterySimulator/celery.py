from celery import Celery

celery_app = Celery('simulations', broker='redis://redis:6379/0')