from django.shortcuts import render
from .models import Student,Company,Message,Verify
from django.http import HttpRequest,HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import *
from django.core import serializers
from gcm.models import get_device_model
import json

def index(request):
   return render(request,'app/register.html',{})        

@csrf_exempt
def verify(request):
	data = json.loads(request.body)
	prn=data["prn"]
	if(Verify.objects.filter(prn=prn).exists()):
		return HttpResponse("Success")
	else:
		return HttpResponse("Failed")

@csrf_exempt
def register_student(request):
	data = json.loads(request.body)
	obj=Student()
	email = data["email"]
	if(Student.objects.filter(email=email).exists()):
		return HttpResponse("Already Registered")
	obj.user=data["name"]
	obj.email=data["email"]
	obj.password=data["password"]
	obj.phone=data["phone"]
	obj.branch=data["branch"]
	obj.average=data["average"]
	obj.placed=data["placed"]
	obj.active_back=data["activeBack"]
	obj.save()
	return HttpResponse("Registered Successfully")

@csrf_exempt
def register_company(request):
	data = json.loads(request.body)
	name=data["name"]	
	if(Company.objects.filter(name=name).exists()):
		return HttpResponse("Already Registered")

	criteria = data["criteria"]
	salary=data["salary"]
	other_details=data["other_details"]
	ppt_date=data["ppt_date"]
	back=data["back"]

	#add to database
	obj=Company()
	obj.name=name
	obj.criteria=criteria
	obj.salary=salary
	obj.other_details=other_details
	obj.ppt_date=ppt_date
	obj.back=back
	obj.save()

	#send notification
	Device = get_device_model()
	Device.objects.all().send_message({'type':'company_reg','name':name,'criteria':criteria,'salary':salary,'other_details':other_details,'ppt_date':ppt_date,'back':back})
	return HttpResponse("Registered Successfully")

@csrf_exempt
def update_company(request):
	data = json.loads(request.body)	
	name=data["name"]
	reg_start=data["reg_start"]
	reg_end=data["reg_end"]
	reg_link=data["reg_link"]
	other_details=data["other_details"]

	obj=Company.objects.get(name=name)
	if(obj.reg_link):
		return HttpResponse("Already Updated")
	obj.reg_start_date=reg_start
	obj.reg_end_date=reg_end
	obj.reg_link=reg_link
	if(obj.other_details and other_details):
		obj.other_details=obj.other_details + " " +  other_details
	elif(other_details):
		obj.other_details=other_details
	obj.save()

	#send notifications
	Device = get_device_model()
	Device.objects.all().send_message({'type':'company_update','name':name,'reg_link':reg_link ,'reg_start':reg_start, 'reg_end':reg_end ,'other_details':other_details})

	return HttpResponse("Company Updated")

@csrf_exempt
def login_details(request):
	data = json.loads(request.body)
	get_mail=data["email"]
	get_pw=data["password"]
	if(Student.objects.filter(email=get_mail).exists()):
		obj=Student.objects.get(email=get_mail)
		if(obj.password==get_pw):
			return HttpResponse(obj.user)
		else:
			return HttpResponse("Incorrect Password")
	else:
		return HttpResponse("User not found")

@csrf_exempt
def sync_data(request):
	objs=Company.objects.all()
	data = serializers.serialize("json", objs)
	print data[1:-1]
	return HttpResponse(data,content_type='json')

@csrf_exempt
def notify(request):
	data = json.loads(request.body)
	title=data["title"]
	body=data["body"]
	obj=Message()
	obj.title=title
	obj.message=body
	obj.save()
	Device = get_device_model()
	Device.objects.all().send_message({'type':'gen_msg','title':title,'body':body})
	return HttpResponse("Message sent")