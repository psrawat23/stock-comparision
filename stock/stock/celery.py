from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock.settings')
app = Celery('stock')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

  

# Celery Beat Settings
# app.conf.beat_schedule = {
# 'send-mail-every-day-at-8':{
# 'task':'celery_task.tasks.say_hi',
# 'schedule':crontab(hour=10,minute=6),
# # 'args':(2,)
# }
# }

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')