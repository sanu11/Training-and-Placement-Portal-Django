
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
import dropbox
import requests

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
	return HttpResponse(obj.user)

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
	obj.reg_start=reg_start
	obj.reg_end=reg_end
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

@csrf_exempt
def get_main_page(request):
	if( not request.session.get("name")):
		login=0
		return render(request,'app/home.html',{"login":login})
	else:
		login=1
		name=request.session["name"]
		return render(request,'app/home.html',{"login":login,"name":name})

@csrf_exempt
def get_signup_page(request):
	return render(request,'app/signup.html',{})

@csrf_exempt
def get_login_page(request):
	print "in login page"
	return render(request,'app/login.html',{})

@csrf_exempt
def get_register_page(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		name=request.session["name"]
		return render(request,'app/register.html',{"name":name})

@csrf_exempt
def get_update_page(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		name=request.session["name"]
		companies=list(Company.objects.all().order_by('-c_id'))
		return render(request,'app/update.html',{"companies":companies,"name":name})

@csrf_exempt
def get_notify_page(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		name=request.session["name"]
		return render(request,'app/notify.html',{"name":name})

@csrf_exempt
def get_notifications_page(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		name=request.session["name"]
		notifications = Message.objects.all().order_by('-msg_id')
		return render(request,'app/notification.html',{"notifications":notifications,"name":name})


@csrf_exempt
def get_statistics_page(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		name=request.session["name"]
		companies = Company.objects.all().order_by('-c_id')
		return render(request,'app/statistics.html',{"companies":companies,"name":name})

@csrf_exempt
def get_students_page(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		name=request.session["name"]
		students = Student.objects.all()
		return render(request,'app/students.html',{"students":students,"name":name})


@csrf_exempt
def logout(request):
	if( not request.session.get("name")):
		return HttpResponse("Please Login")			
	else:
		del request.session['email']
		del request.session['name']
		request.session.modified = True
		print "end"
		return render(request,'app/redirect2.html',{})  
	   
@csrf_exempt
def web_signup(request):
	if request.method=="POST":
		email=request.POST["email"]
		name=request.POST["name"]
		roll=request.POST["roll"]
		print name,email
		if(Student.objects.filter(email=email).exists()):
			return HttpResponse('Already Registered')
		c=Student()
		c.user=name
		c.email=email
		c.password=request.POST["password"]
		c.roll=roll
		c.phone=request.POST["phone"]
		c.branch=request.POST["branch"]
		c.ssc=request.POST["10th"]
		c.hsc=request.POST["12th"]
		c.average=request.POST["average"]

		# c.activeBack=request.POST.get("activeBack")
		dbx = dropbox.Dropbox('Lae_eeDcmDgAAAAAAAACpAf6K4pN2cMT9Pa3UcARF6HVT5kbljzzyo7DazeUtE9D')
		st = dbx.users_get_current_account()
		for entry in dbx.files_list_folder('').entries:
			print(entry.name)
		if request.FILES["resume"]:
			myfile = request.FILES["resume"]
			data=myfile.read()
			filename=myfile.name
			extension=filename.split('.')
			file_to="/"+roll+'.'+extension[1]
			print file_to   
			dbx.files_upload(data, file_to)
			
			url = "https://api.dropboxapi.com/2/sharing/create_shared_link"
		
			payload = "{\"path\":"+ '"' + file_to + '"' + ",\"short_url\": true}"
			print payload
			headers = {
			'authorization': "Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR",
			'content-type': "application/json",
			'cache-control': "no-cache",
			}

			response = requests.request("POST", url, data=payload, headers=headers)

			res=json.loads(response.text)
			url=res["url"]
			c.url=url
			c.save()

		request.session['email']= email          #send cookie
		request.session['name']=name
		return render(request,'app/login.html',{})
	else:
		return HttpResponse('Error');

@csrf_exempt
def web_login(request):
	if request.method=="POST":
		get_mail=request.POST.get("email")
		get_pw=request.POST.get("password")
	
		if(Student.objects.filter(email=get_mail).exists()):
			obj=Student.objects.get(email=get_mail)
			if(obj.password==get_pw):
				name=obj.user
				request.session['email']= get_mail 
				request.session['name']=name
				return render(request,'app/redirect.html',{})
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
		ppt_time=request.POST["ppt_time"]
		other_details=request.POST["other_details"]
		if(other_details==""):
			other_details=None
 #add to database
		obj=Company()
		obj.name=name
		obj.criteria=criteria
		obj.salary=salary
		obj.other_details=other_details
		obj.ppt_date=ppt_date + " " + ppt_time
		obj.back=back
		obj.save()

		
    	#send notification
		Device = get_device_model()

		Device.objects.all().send_message({'type':'company_reg','name':name,'criteria':criteria,'salary':salary,'other_details':other_details,'ppt_date':ppt_date,'back':back})
		name=request.session["name"]
		return render(request,'app/home.html',{"name":name,"login":1})
	else:
		return HttpResponse("Error")

@csrf_exempt
def web_update_company(request):
	if request.method=="POST":
		name=request.POST["name"]
		reg_link=request.POST["regLink"]
		reg_start_date=request.POST["regStartDate"]
		reg_start_time=request.POST["regStartTime"]
		reg_end_date=request.POST["regEndDate"]
		reg_end_time=request.POST["regEndTime"]
		other_details=request.POST["otherDetails"]
		obj=Company.objects.get(name=name)
		if(obj.reg_link):
			return HttpResponse("Already Updated")
		reg_start=reg_start_date + " " + reg_start_time
		reg_end =reg_end_date + " " + reg_end_time
		print reg_start , reg_end
		obj.reg_start=reg_start
		obj.reg_end=reg_end
		obj.reg_link=reg_link
		if(obj.other_details and other_details):
			obj.other_details=obj.other_details + " " +  other_details
		elif(other_details):
			obj.other_details=other_details
		obj.save()

    #send notifications
		Device = get_device_model()
		Device.objects.all().send_message({'type':'company_update','name':name,'reg_link':reg_link ,'reg_start':reg_start, 'reg_end':reg_end ,'other_details':other_details})
		name=request.session["name"]
		return render(request,'app/home.html',{"name":name,"login":1})
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
		
		name=request.session["name"]
		return render(request,'app/home.html',{"name":name,"login":1})
	else:
		return HttpResponse("Error")


		