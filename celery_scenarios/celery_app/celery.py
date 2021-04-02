from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab

app = Celery('celery_uncovered')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('celery_scenarios.config.base')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'perform-my-priodic-task': {
        'task': 'celery_scenarios.workflow.my_workflow',
        'schedule': crontab(minute='*/1'),
    },
}
