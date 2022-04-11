from django.db import models
import datetime
import os
from django.conf import settings
def filePath(request, filename):
    # timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    # filename = "%s%s" % (timeNow, old_file)
    pathname = os.path.join(filename)
    return pathname

# Create your models here.
class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile = models.CharField(max_length=15)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

class PredictImage(models.Model):
    img_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to=filePath, null=True, blank=True)