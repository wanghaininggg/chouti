from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32, db_index=True)
    email = models.CharField(max_length=32, unique=True)
    pwd = models.CharField(max_length=64)
    ctime = models.DateTimeField(auto_now_add=True)

class SendMsg(models.Model):
    email = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=6)
    stime = models.DateTimeField()
    times = models.IntegerField()
