from django.shortcuts import render
from .models import Student,Company
from django.http import HttpRequest,HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import *
from gcm.models import get_device_model

import json
def index(request):
   return render(request,'app/register.html',{})        

@csrf_exempt
def register_student(request):
	# if(request.method=="POST"):
	data = json.loads(request.body)
	obj=Student()
	obj.user=data["name"]
	obj.email=data["email"]
	obj.password=data["password"]
	obj.phone=data["phone"]
	obj.branch=data["branch"]
	obj.average=data["average"]
	obj.placed=data["placed"]
	obj.active_back=data["activeBack"]
	obj.save()
	return HttpResponse("Data saved")

@csrf_exempt
def register_company(request):
	data = json.loads(request.body)
	obj=Company()
	obj.name=data["name"]
	obj.criteria=data["criteria"]
	obj.salary=data["salary"]
	obj.other_details=data["other_details"]
	obj.ppt_date=data["ppt_date"]
	obj.back=data["back"]
	obj.save()
	return HttpResponse("Data saved")
# Create your views here.

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
def message(request):
	data = json.loads(request.body)
	get_msg=data["message"]


@csrf_exempt
def notify(request):
	data = json.loads(request.body)
	title=data["title"]
	body=data["body"]
	Device = get_device_model()
	Device.objects.all().send_message({'title':title,'body':body})