from django.db import models

class newusers(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

    objects=models.Manager()

class formusers(models.Model):
    bktype=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    age=models.IntegerField()
    dob=models.DateField()
    phone=models.CharField(max_length=20)
