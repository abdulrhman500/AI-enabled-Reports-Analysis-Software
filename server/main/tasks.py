from background_task import background
from main.models import Patch
import datetime
import os
@background()
def my_scheduled_task():

    print("Executing scheduled task now...")
    patches = Patch.objects.all()
    oneOpen = False

    for p in patches:
        today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        close_date = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0, day=p.close_date.day,month=p.close_date.month,year=p.close_date.year)
        start_date = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0, day=p.start_date.day,month=p.start_date.month,year=p.start_date.year)
        
        if close_date < today:
            p.open = False
            p.save()
            directory = p.semester
  
            # Parent Directory path 
            parent_dir = "uploads"
            
            # Path 
            path = os.path.join(parent_dir, directory) 
            try:
                os.makedirs(path, exist_ok = True) 
                print("Directory '%s' created successfully" % directory) 
            except OSError as error: 
                print("Directory '%s' can not be created" % directory) 
        
        if oneOpen:
            continue

        if start_date > today:
            p.open = True
            p.save()
            oneOpen = True
    
    print("Finished executing task.")