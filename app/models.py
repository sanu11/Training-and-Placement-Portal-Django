from __future__ import unicode_literals

from django.db import models
#Create your models here.

class Year(models.Model):
	y_id		=	models.AutoField(primary_key=True)
	year		=	models.CharField(max_length=50,unique=True)
	total		=	models.IntegerField()
	comp		=	models.IntegerField()
	it			=	models.IntegerField()
	entc		=	models.IntegerField()
	total_placed=	models.IntegerField(null=True,blank=True)
	comp_placed	=	models.IntegerField(null=True,blank=True)
	it_placed	=	models.IntegerField(null=True,blank=True)
	entc_placed	=	models.IntegerField(null=True,blank=True)

	def __str__(self):
		return  self.year

class Company(models.Model):

	c_id		=	models.AutoField(primary_key=True)
	name		=	models.CharField(max_length=40)
	criteria	=	models.FloatField(blank=True,null=True)
	back		=	models.CharField(max_length=100,blank=True,null=True)
	position    =   models.CharField(max_length=30,null=True,blank=True)
	salary      =   models.FloatField(blank=True, null=True)
	ppt_date	=	models.DateTimeField(null=True,blank=True)
	hired_count = 	models.IntegerField(null=True,blank=True)
	other_details=	models.CharField(max_length=1000,null=True,blank=True)
	placed_url =	models.CharField(max_length=500, null=True, blank=True)
	reg_start	=	models.DateTimeField(null=True,blank=True)
	reg_end		=	models.DateTimeField(null=True,blank=True)
	reg_link	=	models.CharField(max_length=1000,null=True,blank=True)
	y_id		=	models.ForeignKey(Year,null=True,blank=True)															 #foreign key to year table

	def __str__(self):
		if self.position:
			return  self.name + "("+ self.position + ")"
		else:
			return  self.name

class Student(models.Model):

	s_id		=	models.AutoField(primary_key=True)
	college_id	=	models.CharField(max_length=20,unique=True)
	prn			=	models.CharField(max_length=20,unique=True)
	roll		= 	models.IntegerField()
	name        =	models.CharField(max_length=50)
	email       =	models.EmailField(max_length=60,unique=True)
	password    =	models.CharField(max_length=12)
	phone       =	models.CharField(max_length=10)
	gender      =	models.CharField(max_length=10)
	per_address =	models.CharField(max_length=1000,null=True,blank=True)
	cur_address =	models.CharField(max_length=1000,null=True,blank=True)
	y_id        =	models.ForeignKey(Year)            												 #foreign key to year table
	branch		=	models.CharField(max_length=6)
	tenth_board =	models.CharField(max_length=20)
	tenth_marks	=	models.FloatField()
	tenth_yeargap=  models.BooleanField()
	tenth_yeargap_reason=models.CharField(max_length=50)
	is_diploma	=	models.BooleanField()
	twelveth_board= models.CharField(max_length=20,null=True,blank=True)
	twelveth_marks=	models.FloatField(null=True,blank=True)
	twelveth_yeargap=models.BooleanField()
	twelveth_yeargap_reason=models.CharField(max_length=50)
	diploma_marks=	models.FloatField(null=True,blank=True)
	average		=	models.FloatField()
	aadhar_number=	models.CharField(max_length=20)
	placed		=	models.BooleanField(default=False)
	active_back	=	models.BooleanField(default=False)
	url			=	models.CharField(max_length=500,null=True,blank=True)
	c_id		=	models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)			#foreign key o company table

	def __str__(self):
		return  self.name

class Admin(models.Model):
	name		  =	models.CharField(max_length=50)
	email		  =	models.EmailField(max_length=60,unique=True)
	password	  =	models.CharField(max_length=12)
	other_details =	models.CharField(max_length=1000,null=True,blank=True)

	def __str__(self):
		return  self.name


# class Profile(models.Model):
#
# 	p_id		=	models.AutoField(primary_key=True)
# 	position	=	models.CharField(max_length=50,null=True,blank=True)
# 	salary		=	models.FloatField(blank=True, null=True)
# 	hired_count	=	models.IntegerField(default=0)
# 	c_id		=	models.ForeignKey(Company,on_delete=models.CASCADE)			#Foreign key on company
#
# 	def __str__(self):
# 		return	Company.name + " " + self.position

class Verify(models.Model):
	v_id		=	models.AutoField(primary_key=True)
	prn			=	models.CharField(max_length=50)
	college_id  =   models.CharField(max_length=20)

	def __str__(self):
		return self.prn

class Message(models.Model):
	msg_id		=	models.AutoField(primary_key=True)
	title		=	models.CharField(max_length=200,default="")
	message		=	models.CharField(max_length=10000,default="",null=True,blank=True)
	url			=	models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return self.title


class Result(models.Model):
	r_id		=	models.AutoField(primary_key=True)
	c_id		=	models.ForeignKey(Company,on_delete=models.CASCADE)			#foreign key o company table
	shortlist 	=	models.CharField(max_length=100)
	filename	=	models.CharField(max_length=100)
	url 		=	models.CharField(max_length=100)
	other_details= models.CharField(max_length=1000)

	def __str__(self):
		return self.filename

