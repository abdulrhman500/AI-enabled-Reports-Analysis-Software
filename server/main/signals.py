from django.db.models.signals import post_migrate
from django.dispatch import receiver
from background_task.models import Task
from .tasks import my_scheduled_task
import datetime

@receiver(post_migrate)
def run_initial_background_task(sender, **kwargs):
    print('checking task exists')
    # Check if the task already exists
    if not Task.objects.filter(task_name='main.tasks.my_scheduled_task').exists():
        # Schedule the task to run immediately (you can adjust this)
        print('task created')
        my_scheduled_task(repeat=Task.DAILY)

run_initial_background_task('me')