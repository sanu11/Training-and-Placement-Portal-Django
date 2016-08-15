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
	if(request.method=="POST"):
		obj=Company()
		obj.id=request.POST["id"]
		obj.name=request.POST["name"]
		obj.criteria=request.POST["criteria"]
		obj.salary=request.POST["salary"]
		obj.reg_start_date=request.POST["reg_start_date"]
		obj.reg_end_date=request.POST["reg_end_date"]
		obj.ppt_date=request.POST[ppt_date]
		obj.apti_date=request.POST["apti_date"]
		obj.interview_date=request.POST["interview_date"]
		obj.last_date=request.POST["last_date"]
		obj.hired_people=request.POST["hired_people"]
		obj.save()
		return HttpResponse("Data saved")
# Create your views here.