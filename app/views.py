from django.shortcuts import render
from .models import Student,Company
from django.http import HttpRequest,HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import *
def index(request):
   return render(request,'app/register.html',{})        

@csrf_exempt
def register_student(request):
	if(request.method=="POST"):
		obj=Student()
		obj.user=request.POST.get("name")
		obj.email=request.POST.get("email")
		obj.password=request.POST.get("password")
		obj.address=request.POST.get("address")
		obj.phone=request.POST.get("phone")
		obj.branch=request.POST.get("branch")
		obj.average=request.POST.get("average")
		obj.placed=request.POST.get("placed")
		obj.active_back=request.POST.get("active_back")
		obj.num_back=request.POST.get("num_back")
		# print obj.user ,obj.email,obj.password,obj.address,obj.phone,obj.branch,obj.average,obj.placed,obj.num_back,obj.active_back
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