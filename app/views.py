from django.shortcuts import render
from .models import Student,Company
from django.http import HttpRequest,HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import *
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
	obj.reg_start_date=data["reg_start_date"]
	obj.reg_end_date=data["reg_end_date"]
	obj.ppt_date=data[ppt_date]
	obj.apti_date=data["apti_date"]
	obj.interview_date=data["interview_date"]
	# obj.last_date=data["last_date"]
	obj.hired_people=data["hired_people"]
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



