
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
	obj.active_back=data["activeBack"]
	obj.save()
	return HttpResponse("Success")

@csrf_exempt
def login_details(request):
	data = json.loads(request.body)
	get_mail=data["email"]
	get_pw=data["password"]
	if(Student.objects.filter(email=get_mail).exists()):
		obj=Student.objects.get(email=get_mail)
		if(obj.password==get_pw):
			return HttpResponse("Success")
		else:
			return HttpResponse("Incorrect Password")
	else:
		return HttpResponse("User not found")


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
	return HttpResponse("Success")

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
def sync_data(request):
	objs=Company.objects.all()
	data = serializers.serialize("json", objs)
	print data[1:-1]
	return HttpResponse(data,content_type='json')

@csrf_exempt
def notify(request):
	data = json.loads(request.body)
	print data
	title=data["title"]
	body=data["body"]
	obj=Message()
	obj.title=title
	obj.message=body
	obj.save()
	Device = get_device_model()
	Device.objects.all().send_message({'type':'gen_msg','title':title,'body':body})
	return HttpResponse("Message sent")


###WEB###


def index(request):
   return render(request,'app/index.html',{})  

@csrf_exempt
def get_main_page(request):
	companies=list(Company.objects.all().order_by('-c_id'))
	return render(request,'app/main.html',{"companies":companies})

@csrf_exempt
def get_signup_page(request):
	return render(request,'app/upload.html',{})

@csrf_exempt
def get_login_page(request):
	print "in login page"
	return render(request,'app/login.html',{})

@csrf_exempt
def get_register_page(request):
	return render(request,'app/upload.html',{})

@csrf_exempt
def get_update_page(request):
	companies=list(Company.objects.all().order_by('-c_id'))
	return render(request,'app/update.html',{"companies":companies})

@csrf_exempt
def get_notify_page(request):
	return render(request,'app/notify.html',{})

@csrf_exempt
def get_notifications_page(request):
	notifications = Message.objects.all().order_by('-msg_id')
	return render(request,'app/notification.html',{"notifications":notifications})


@csrf_exempt
def get_statistics_page(request):
	companies = Company.objects.all().order_by('-c_id')
	return render(request,'app/notification.html',{"companies":companies})



@csrf_exempt
def logout(request):
	del request.session['email']
	request.session.modified = True
	print "end"
	return render(request,'app/index.html',{})  
   
@csrf_exempt
def web_signup(request):
	if request.method=="POST":
		get_mail=request.POST["email"]
		if(Student.objects.filter(email=get_mail).exists()):
			return HttpResponse('Already Registered')
		c=Student()
		c.name=request.POST["name"]
		mail=request.POST["email"]    
		c.mail=mail
		c.password=request.POST["password"]
		c.phone=request.POST["phone"]
		c.branch=request.POST["branch"]
		c.average=request.POST["average"]
		c.activeBack=request.POST["activeBack"]
		c.save()
		request.session['email']= mail          #send cookie
		return HttpResponse('Success');
	else:
		return HttpResponse('Error');


@csrf_exempt
def web_login(request):
	if request.method=="POST":
		get_mail=request.POST.get("email")
		get_pw=request.POST.get("password")
		st=Student.objects.all()
		companies=list(Company.objects.all().order_by('-c_id'))
		if(Student.objects.filter(email=get_mail).exists()):
			obj=Student.objects.get(email=get_mail)
			if(obj.password==get_pw):
				request.session['email']= get_mail 
				return render(request,'app/main.html',{"companies":companies})
			else:
				return HttpResponse("Incorrect Password")
		else:
			return HttpResponse("User not found")

@csrf_exempt
def web_verify(request):
	if request.method=="POST":
		prn=request.POST["prn"]
		if(Verify.objects.filter(prn=prn).exists()):
			return HttpResponse("Success")
		else:
			return HttpResponse("Failed")

@csrf_exempt
def web_register_company(request):
	if request.method=="POST":
		name=request.POST["name"]
		if(Company.objects.filter(name=name).exists()):
			return HttpResponse('Already Registered')
		name=request.POST["name"]			
		salary=request.POST["salary"]
		criteria=request.POST["criteria"]
		back=request.POST["back"]
		ppt_date=request.POST["ppt_date"]
		other_details=request.POST["other_details"]
		print name," ",salary," ",other_details
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
		return HttpResponse("Success")
	else:
		return HttpResponse("Error")

@csrf_exempt
def web_update_company(request):
	if request.method=="POST":
		name=request.POST["name"]
		reg_link=request.POST["reg_link"]
		reg_start=request.POST["reg_start"]
		reg_end=request.POST["reg_end"]
		other_details=request.POST["other_details"]
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
	return HttpResponse("Error")


@csrf_exempt
def web_notify(request):
	if request.method=="POST":
		title=request.POST["title"]
		body=request.POST["body"]
		obj=Message()
		obj.title=title
		obj.message=body
		obj.save()
		Device = get_device_model()
		Device.objects.all().send_message({'type':'gen_msg','title':title,'body':body})
		return HttpResponse("Message sent")
	else:
		return HttpResponse("Error")




