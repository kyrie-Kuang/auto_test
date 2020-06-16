# coding=utf-8
import time
from celery.task import Task


class ApiTask(Task):
    name = 'api-task'

    def run(self, *args, **kwargs):
        print('start...')
        time.sleep(3)
        print('args={},kwargs={}'.format(args, kwargs))
        print('end...')
