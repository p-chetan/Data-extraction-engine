from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from datetime import datetime, time

from django.db.models.fields import IntegerField


# Create your models here.
class New(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    DXpath = models.CharField(max_length=1000)
    BXpath = models.CharField(max_length=1000)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__ (self):
        return self.name

class Buzz(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    DXpath = models.CharField(max_length=1000)
    BXpath = models.CharField(max_length=1000)
    col = models.IntegerField()
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__ (self):
        return self.name

class PDF(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    pages = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__ (self):
        return self.name

class Sche(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    MIN= models.IntegerField()
    HR= models.IntegerField()
    DAYMONTH= models.IntegerField()
    MONTH= models.IntegerField()
    DAYWEEK= models.IntegerField()

    

    