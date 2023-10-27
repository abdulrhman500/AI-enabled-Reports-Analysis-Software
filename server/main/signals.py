from django.db.models.signals import post_migrate
from django.dispatch import receiver
from background_task.models import Task
from .tasks import my_scheduled_task
import datetime
import pytz
from pytz import timezone

@receiver(post_migrate)
def run_initial_background_task(sender, **kwargs):
    print('checking task exists')
    # Check if the task already exists
    if not Task.objects.filter(task_name='main.tasks.my_scheduled_task').exists():

        today = datetime.datetime.now(timezone('UTC'))
        today=today.astimezone(timezone('Africa/Cairo'))
        date = today.replace(hour=23,minute=15)
        print(date)
        if today > date:
            date += datetime.timedelta(days=1)

        my_scheduled_task(schedule=date,repeat=60)
        print('task created')

run_initial_background_task('me')