from django.shortcuts import render
from .models import Student,Company
from django.http import HttpRequest,HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import *
def index(request):
   return render(request,'samp.html',{})        

@csrf_exempt
def register_student(request):
	if(request.method=="POST"):
		obj=Student()
		obj.name=request.POST["name"]
		obj.email=request.POST["email"]
		obj.password=request.POST["password"]
		obj.address=request.POST["address"]
		obj.phone=request.POST["phone"]
		obj.branch=request.POST["branch"]
		obj.average=request.POST["average"]
		obj.placed=request.POST["placed"]
		obj.active_back=POST["active_back"]
		obj.num_back=POST["num_back"]
		obj.company_id=POST["Company_id"]
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