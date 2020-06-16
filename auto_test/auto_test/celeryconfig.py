# coding=utf-8
from datetime import timedelta

import djcelery

djcelery.setup_loader()

CELERY_QUEUES = {
    'beat_tasks': {
        'exchange': 'beat_tasks',
        'exchange_type': 'direct',
        'binding_key': 'beat_tasks'

    },
    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'

    }
}

CELERY_DEFAULT_QUEUE = 'work_queue'

CELERY_IMPORTS = (
    'api.tasks',
)

CELERYBEAT_SCHEDULE = {
    'task1': {
        'task': 'api-task',
        'schedule': timedelta(seconds=5),
        'options': {
            'queue': 'beat_tasks'
        }
    }
}