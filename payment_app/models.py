from django.db import models
from django.contrib.auth.models import User
# Create your models here.



    
class Group(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    total = models.IntegerField(null=True,blank=True)
    per_person = models.IntegerField(null=True,blank=True)
    users = models.CharField(max_length=100)

class Expenses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    payment = models.IntegerField( default=0, null=True,blank=True)
    msg = models.TextField(null= True,blank=True, default= '' )
    group_name = models.ForeignKey(Group,on_delete=models.CASCADE)