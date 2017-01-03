from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class Student(models.Model):

	# s_id=models.AutoField(primary_key=True)
	college_id=models.CharField(max_length=50)
	user=models.CharField(max_length=50)
	email=models.EmailField(max_length=60,unique=True)
	password=models.CharField(max_length=12)
	phone=models.CharField(max_length=10)
	gender=models.CharField(max_length=10)
	roll=models.IntegerField()
	branch=models.CharField(max_length=6)
	ssc=models.FloatField()
	hsc=models.FloatField()
	average=models.FloatField()
	placed=models.CharField(max_length=4,default="No")
	active_back=models.CharField(max_length=4,default="No")
	url=models.CharField(max_length=500)
	company_id=models.IntegerField(default=-1)
#	resume=models.FileField()

	def __str__(self):
		return  self.email

class Company(models.Model):

	c_id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=40)
	criteria=models.FloatField(blank=True,null=True)
	salary=models.FloatField(blank=True,null=True)
	back=models.CharField(max_length=100,blank=True,null=True)
	ppt_date=models.DateTimeField(null=True,blank=True)
	other_details=models.CharField(max_length=1000,null=True,blank=True)
	
	reg_start=models.DateTimeField(null=True,blank=True)
	reg_end=models.DateTimeField(null=True,blank=True)
	reg_link=models.CharField(max_length=1000,null=True,blank=True)
	hired_people=models.IntegerField(default=0)

	#apti_date=models.DateTimeField(null=True,blank=True)
	#last_date=models.DateTimeField()
	def __str__(self):
		return  self.name


class Verify(models.Model):
	v_id=models.AutoField(primary_key=True)
	prn=models.CharField(max_length=50)

	def __str__(self):
		return self.prn

class Message(models.Model):

	msg_id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=200,default="")
	message=models.CharField(max_length=10000,default="")
	
	def __str__(self):
		return self.title