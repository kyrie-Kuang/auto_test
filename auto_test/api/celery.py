from __future__ import absolute_import
import django
import os
from celery import Celery
from django.conf import settings

# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_test.settings')
django.setup()


app = Celery('auto_test')

app.config_from_object('django.conf:settings')
# 发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)