from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class Student(models.Model):
	user=models.CharField(max_length=50)
	email=models.EmailField(max_length=60,unique=True)
	password=models.CharField(max_length=12)
	phone=models.CharField(max_length=10)
	branch=models.CharField(max_length=6)
	average=models.FloatField()
	placed=models.CharField(max_length=4,default="No")
	active_back=models.CharField(max_length=4,default="No")
	company_id=models.IntegerField(default=-1)
#	resume=models.FileField()

	def __str__(self):
		return  self.email

class Company(models.Model):
	c_id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=40)
	criteria=models.FloatField()
	salary=models.IntegerField()
	other_details=models.CharField(max_length=1000,default="")
	reg_start_date=models.DateTimeField()
	reg_end_date=models.DateTimeField()
	ppt_date=models.DateTimeField()
	apti_date=models.DateTimeField()
	interview_date=models.DateTimeField()
	# last_date=models.DateTimeField()
	hired_people=models.IntegerField(default=0)

	def __str__(self):
		return  self.name

class Message(models.Model):
	msg_id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=200,default="")
	message=models.CharField(max_length=10000,default="")
	
	def __str__(self):
		return self.title