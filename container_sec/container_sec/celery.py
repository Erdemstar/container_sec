from django.conf import settings

from container_sec.settings import APP_IMAGESCAN_PATH
from celery import Celery
import subprocess
import os
import json


# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'container_sec.settings')

# you can change the name here
app = Celery("appsec")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(serializer='json')
def task_image_scan (image_name,result_path,result_name,dockerfile_path=None):
    command = "grype {} -o json >>{}{}".format(image_name,result_path,result_name) 
    #command = "grype {} -o json".format(image_name)
    response = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return json.dumps(response.decode("utf-8"))
    print (image_name + " is scanning with success")


# Dockerfile ve İmagescan result kısmını günlük silecek bir schedule task yaz