import datetime
from django.utils import timezone
from django.shortcuts import render , redirect
from django.template.loader import render_to_string 
from .models import Student, Company, Message, Verify, Result, Admin ,Year
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import *
from django.core import serializers
from gcm.models import get_device_model
from django.http import StreamingHttpResponse
import json,csv
import dropbox
import requests
import io
import random,string
from djqscsv import render_to_csv_response,write_csv

@csrf_exempt
def verify(request):
    data = json.loads(request.body)
    prn = data["prn"]
    if Verify.objects.filter(prn=prn).exists():
        return HttpResponse("Success")
    else:
        return HttpResponse("Failed")

@csrf_exempt
def register_student(request):
    data = json.loads(request.body)
    obj = Student()
    email = data["email"]
    if Student.objects.filter(email=email).exists():
        return HttpResponse("Already Registered")
    obj.name = data["name"]
    obj.email = data["email"]
    obj.password = data["password"]
    obj.phone = data["phone"]
    obj.branch = data["branch"]
    obj.average = data["average"]
    obj.active_back = data["activeBack"]
    obj.save()
    return HttpResponse(obj.name)


@csrf_exempt
def login_details(request):
    data = json.loads(request.body)
    get_mail = data["email"]
    get_pw = data["password"]
    if Student.objects.filter(email=get_mail).exists():
        obj = Student.objects.get(email=get_mail)
        if obj.password == get_pw:
            return HttpResponse("Student,"+obj.name)
        else:
            return HttpResponse("Incorrect Password")
    
    elif Admin.objects.filter(email=get_mail).exists():
        obj = Admin.objects.get(email=get_mail)
        if obj.password == get_pw:
            return HttpResponse("Admin,"+obj.name)
        else:
            return HttpResponse("Incorrect Password")

    else:
        return HttpResponse("User not found")


@csrf_exempt
def register_company(request):
    data = json.loads(request.body)
    name = data["name"]
    if "position" in data:
        position = data["position"]
    else:
        position = "NA"
    criteria = data["criteria"]
    salary = data["salary"]
    other_details = data["other_details"]
    ppt_date = data["ppt_date"]
    back = data["back"]

    # add to database
    obj = Company()
    obj.name = name
    obj.position = position
    obj.other_details = other_details
    obj.ppt_date = ppt_date
    obj.back = back
    obj.save()

    # send notification
    Device = get_device_model()
    Device.objects.all().send_message(
        {'type': 'company_reg', 'name': name, 'criteria': criteria, 'salary': salary, 'other_details': other_details,
         'ppt_date': ppt_date, 'back': back})
    return HttpResponse("Success")

@csrf_exempt
def update_company(request):
    data = json.loads(request.body)
    name = data["name"]
    reg_start = data["reg_start"]
    reg_end = data["reg_end"]
    reg_link = data["reg_link"]
    other_details = data["other_details"]

    obj = Company.objects.get(name=name)
    obj.reg_start = reg_start
    obj.reg_end = reg_end
    obj.reg_link = reg_link
    if obj.other_details and other_details:
        obj.other_details = obj.other_details + " " + other_details
    elif other_details:
        obj.other_details = other_details
    obj.save()

    # send notifications
    Device = get_device_model()
    Device.objects.all().send_message(
        {'type': 'company_update', 'name': name, 'reg_link': reg_link, 'reg_start': reg_start, 'reg_end': reg_end,
         'other_details': other_details})

    return HttpResponse("Company Updated")


@csrf_exempt
def sync_data(request):
    objs = Company.objects.all()
    data = serializers.serialize("json", objs)
    print data[1:-1]
    return HttpResponse(data, content_type='json')


@csrf_exempt
def notify(request):
    data = json.loads(request.body)
    print data
    title = data["title"]
    body = data["body"]
    obj = Message()
    obj.title = title
    obj.message = body
    obj.save()
    Device = get_device_model()
    Device.objects.all().send_message({'type': 'gen_msg', 'title': title, 'body': body})
    return HttpResponse("Message sent")

####################
########WEB########
###################

@csrf_exempt
def get_main_page(request):
    if not request.session.get("name"):
        login = 0
        return render(request, 'app/home.html', {"login": login})
    else:
        print  request.session.get_expire_at_browser_close()
        name = request.session["name"]
        get_mail = request.session["email"]
        # admin login
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
            return render(request, 'app/home.html', {"login": login, "name": name})

        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
            student = Student.objects.get(email=get_mail)
            lock = student.lock
            return render(request, 'app/home.html', {"login": login, "name": name,"lock":lock})

@csrf_exempt
def get_developers_page(request):
    if  request.session.get("name"):
        name = request.session["name"]
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
            name = request.session["name"]
            return render(request, 'app/developers.html', {"login": login, "name": name})
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
            student = Student.objects.get(email=get_mail)
            lock = student.lock
            return render(request, 'app/developers.html', {"login": login, "name": name, "lock": lock})
    else:
        login = 0
        name=""
    return render(request, 'app/developers.html', {"login":login,"name":name})

@csrf_exempt
def get_settings_page(request):
    if  request.session.get("name"):
        name = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        resume = student.url
        login = 2
        return render(request, 'app/settings.html', {"login":login,"name":name,"resume":resume})
    else:
        return render(request,'app/redirect2.html',{})

@csrf_exempt
def get_signup_page(request):
    years = list(Year.objects.all().order_by('-y_id'))
    print ("hello")
    return render(request, 'app/signup.html', {"years":years})


@csrf_exempt
def get_login_page(request):
    print "in login page"
    if request.session.get("email"):
        return get_main_page(request)
    else:
        return render(request, 'app/login.html', {})

@csrf_exempt
def get_resume_upload_page(request):
    name = request.session["name"]
    email = request.session["email"]
    student = Student.objects.get(email=email)
    if len(str(student.url))>1:
        resume = student.url
    else:
        resume = None
    return render(request, 'app/resumeUpload.html',{"login":2,"name":name,"resume":resume})


######### student profile pages#####

@csrf_exempt
def get_edit_profile_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        name = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        years = Year.objects.all()
        return render(request, 'app/editProfile.html',{"login":2,"name":name,"student":student,"years":years})

@csrf_exempt
def get_edit_ssc_marks_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        name = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        return render(request, 'app/studentSscMarks.html',{"login":2,"name":name,"student":student})


@csrf_exempt
def get_edit_hsc_marks_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        name = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        return render(request, 'app/studentHscMarks.html',{"login":2,"name":name,"student":student})

@csrf_exempt
def get_edit_be_marks_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        name = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        return render(request, 'app/studentBeMarks.html',{"login":2,"name":name,"student":student})

@csrf_exempt
def get_edit_other_details_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        name = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        birth_date = str(student.birth_date)
        print birth_date
       
        return render(request, 'app/studentOtherdetails.html',{"login":2,"name":name,"student":student,"birth_date":birth_date})


#####UPLOAD pages
@csrf_exempt
def get_register_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            years = Year.objects.all()
            curr_year = Year.objects.order_by('-y_id')[0]
            return render(request, 'app/companyRegister.html',{"name":name,"years":years,"curr_year":curr_year})

        # student login
        else:
            return HttpResponse("Not permitted to access")

@csrf_exempt
def get_student_download_page(request):
    email = request.session["email"]
    student = Student.objects.get(email=email)

    return render(request,'app/studentDetails.html',{"student":student,"lock":-1})

@csrf_exempt
def get_update_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            year = Year.objects.order_by('-y_id')[0]
            companies = Company.objects.filter(y_id=year).order_by('-c_id')
            return render(request, 'app/companyUpdate.html', {"companies": companies, "name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")

def get_company_edit_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]

            year = Year.objects.order_by('-y_id')[0]
            companies = Company.objects.filter(y_id=year).order_by('-c_id')
            return render(request, 'app/companyEdit.html', {"companies": companies, "name": name,"year":year})

        # student login
        else:
            return HttpResponse("Not permitted to access")

@csrf_exempt
def get_notify_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            return render(request, 'app/notify.html', {"name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")


@csrf_exempt
def get_result_upload_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            year = Year.objects.all().order_by('-y_id')[0]
            companies = list(Company.objects.filter(y_id=year).order_by('-c_id'))
            return render(request, 'app/resultUpload.html', {"companies": companies, "name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")

@csrf_exempt
def get_company_details(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            c_id = request.POST["company"]
            print c_id
            year = Year.objects.order_by('-y_id')[0]
            obj = Company.objects.get(c_id=c_id,y_id=year)
            data = serializers.serialize("json", [obj,])
            return HttpResponse(data)

        # student login
        else:
            return HttpResponse("Not permitted to access")


@csrf_exempt
def get_search_student_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            years = Year.objects.all()
            year = years.order_by('-y_id')[0]
            name = request.session["name"]
            return render(request,'app/searchStudent.html',{"years":years,"year":year,"name":name})
        else:
            return HttpResponse("Not permitted to access")


@csrf_exempt
def get_student_details(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            years = Year.objects.all()
            year = str(request.POST["year"])
            print year
            if year != "All":
                year = Year.objects.get(year=year)
            else:
                year = Year.objects.all()[0]
                        
            roll  = request.POST["roll"]
            if not Student.objects.filter(roll=roll,y_id=year).exists():
                return HttpResponse("Student not found")
            obj = Student.objects.get(roll=roll,y_id=year)
            context = {}
            context["student"]=obj
            context["lock"] = obj.lock
            # print obj.lock
            return render(request,"app/studentDetails.html",context)
        else:
            return HttpResponse("Not permitted to access")



#######DISPLAY Pages######


@csrf_exempt
def get_students_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            year = "All"
            branch = "All"

            if  "year"  in request.POST:
                year = str(request.POST["year"])
                if year != "All":
                    yearobj = Year.objects.get(year=year)
                    students_year = Student.objects.filter(y_id=yearobj)
                else:
                    students_year = Student.objects.all()
            else:
                students_year = Student.objects.all()

            if  "branch" in request.POST:
                branch = request.POST["branch"]
                if branch != "All":
                    students_branch = students_year.filter(branch=branch)
                else:
                    students_branch = students_year
            else:
                students_branch = students_year

            minavg = 0
            maxavg=100
            lock_status = "All"
            
            if "minavg" in request.POST:
                minavg = request.POST["minavg"]
                students_min_average = students_branch.filter(average__gte = minavg)
            else:
                students_min_average = students_branch

            if "maxavg" in request.POST:
                maxavg = request.POST["maxavg"]
                students_max_average = students_min_average.filter(average__lte= maxavg)
            else:
                students_max_average = students_min_average

            if "lock" in request.POST:
                lock_status = request.POST["lock"]
                if lock_status == "locked":
                    students_lock_status = students_max_average.filter(lock=1)
                elif lock_status == "unlocked":
                    students_lock_status = students_max_average.filter(lock=0)
                else:
                    students_lock_status = students_max_average
            else:
                students_lock_status = students_max_average

            students = students_lock_status
            years = Year.objects.all().order_by('-y_id')

            print students
            name = request.session["name"]
            return render(request, 'app/students.html', {"students": students, "years":years ,"year":year,"branch":branch,"minavg":minavg,"maxavg":maxavg,"lock":lock_status,"name": name})
        # student login
        else:
            return HttpResponse("Not permitted to access")

#handled using ajax
@csrf_exempt
def get_student_page(request, roll):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            if Student.objects.filter(roll=roll).exists():
                student = Student.objects.get(roll=roll)
                return render(request, 'app/studentDetails.html', {"student": student, "name": name})
            else:
                return HttpResponse("Not Found")
        # student login
        else:
            return HttpResponse("Not permitted to access")


###Accessible to students
@csrf_exempt
def get_notifications_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
            lock=0
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
            student = Student.objects.get(email=get_mail)
            lock = student.lock
        name = request.session["name"]
        notifications = Message.objects.all().order_by('-msg_id')
        return render(request, 'app/notification.html', {"notifications": notifications, "name": name, "login": login,"lock":lock})


@csrf_exempt
def get_companies_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
            lock=1
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
            student = Student.objects.get(email=get_mail)
            lock = student.lock
        minsal = 0
        maxsal = 50
        mincri = 0
        maxcri = 100

        curr_year = Year.objects.order_by('-y_id')[0]
        prev_year = None
        if (Year.objects.all().count() > 1):
            prev_year = Year.objects.order_by('-y_id')[1]
        print prev_year
        #year
        if "year" in request.POST:
            year = request.POST["year"]

            if year == curr_year.year and login == 2:
                return HttpResponse("Can't access current year's data")
            year_obj = Year.objects.get(year=year)

        else:
            if login == 2:
                if prev_year:
                    year_obj = Year.objects.order_by('-y_id')[1]

                else:
                    return HttpResponse("No data")
            else:
                year_obj = Year.objects.order_by('-y_id')[0]


        companies_year = Company.objects.filter(y_id=year_obj)
        print  companies_year


        ##min salary
        if "minsal" in request.POST:
            minsal = int(request.POST["minsal"])
            maxsal = int(request.POST["maxsal"])
            if minsal ==  0 and maxsal == 50:
                companies_max_salary = companies_year

            else:
                companies_min_salary = companies_year.filter(salary__gte=minsal)
                companies_max_salary = companies_min_salary.filter(salary__lte=maxsal)

        else:
            companies_max_salary = companies_year

        ##min criteria
        if "mincri" in request.POST:
            mincri = int(request.POST["mincri"])
            maxcri = int(request.POST["maxcri"])
            print mincri , maxcri
            if mincri == 0 and maxcri == 100:
                companies_max_criteria = companies_max_salary
            else:
                companies_min_criteria = companies_max_salary.filter(criteria__gte=mincri)
                companies_max_criteria = companies_min_criteria.filter(criteria__lte=maxcri)
        else:
            companies_max_criteria = companies_max_salary

        companies = companies_max_criteria.order_by('ppt_date')
        years = Year.objects.all()
        name = request.session["name"]
    return render(request, 'app/companies.html', {"companies": companies,"years":years,"year":year_obj,"minsal":minsal ,"maxsal":maxsal,"mincri":mincri, "maxcri":maxcri ,"name": name, "login": login,"lock":lock})

@csrf_exempt
def get_applied_students_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    email = request.session["email"]
    if Admin.objects.filter(email=email).exists():
        name = request.session["name"]
        year = Year.objects.all().order_by('-y_id')[0]
        companies = Company.objects.filter(y_id=year).order_by('-ppt_date')
        login = 1
        return render(request,'app/appliedStudents.html',{"companies":companies,"login":login,"name":name})
    else:
        return HttpResponse("Not permitted to access")

@csrf_exempt
def web_view_students(request,c_id):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    email = request.session["email"]
    if Admin.objects.filter(email=email).exists():
        student_name = request.session["name"]
        company = Company.objects.get(c_id=c_id)
        students = company.applied_students.all()

        login = 1
        print students
        return render(request,'app/viewStudents.html',{"students":students,"login":login,"name":student_name,"company":company})
    else:
        return HttpResponse("Not permitted to access")

def get_opportunities_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        name  = request.session["name"]
        email = request.session["email"]
        student = Student.objects.get(email=email)
        curr_year = Year.objects.order_by('-y_id')[0]
        companies = Company.objects.filter(y_id=curr_year).order_by('-ppt_date')
        for company in companies:
            if company.lock:
                company.status="Closed"
            elif company.reg_end and company.reg_end < timezone.now():
                company.status = "Ongoing"
            elif company.reg_end and company.reg_end > timezone.now() and not company.lock:
                company.status = "Open"
            company.save()

        arr_list = student.company_set.all()
        lock = student.lock
        login = 2
        return render(request,'app/opportunities.html',{"name":name,"companies":companies,"arr_list":arr_list,"login":login,"lock":lock})
    
@csrf_exempt
def get_results_page(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
            lock=0
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
            student= Student.objects.get(email=get_mail)
            lock =student.lock
        name = request.session["name"]
        results = Result.objects.all().order_by('-r_id')
        print results
        return render(request, 'app/results.html', {"results": results, "name": name, "login": login,"lock":lock})


@csrf_exempt
def get_company_page(request, cid):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
        name = request.session["name"]
        if Company.objects.filter(c_id=cid).exists():
            company = Company.objects.get(c_id=cid)
            return render(request, 'app/companyDisplay.html', {"company": company, "name": name, "login": login})
        else:
            return HttpResponse("Not Found")

def get_placed_students_page(request,cid):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    get_mail = request.session["email"]
    if Admin.objects.filter(email=get_mail).exists():
        login = 1
        print "Admin login"
    # student login
    elif Student.objects.filter(email=get_mail).exists():
        login = 2
        print "Student login"
    name = request.session["name"]
    company = Company.objects.get(c_id=cid)
    placed_students = company.student_set.all()
    return  render(request,'app/placedStudents.html',{"students":placed_students,"companyName":company.name,"login":login,"name":name})

@csrf_exempt
def logout(request):
    if not request.session.get("name"):
        return render(request,'app/redirect2.html',{})
    else:

        del request.session['email']
        del request.session['name']
        request.session.modified = True
        print "end"
        return render(request, 'app/redirect2.html', {})



#####upload STUDENTS#####
########################################
########################################

@csrf_exempt
def web_signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        roll = request.POST["roll"]
        print name, email
        if Student.objects.filter(email=email).exists():
            return HttpResponse('exists')
        c = Student()
        c.name = name
        c.email = email
        c.password = request.POST["password"]
        c.gender = request.POST["gender"]
        c.roll = roll
        c.college_id = request.POST["college_id"]
        c.phone = request.POST["phone"]
        c.branch = request.POST["branch"]
        year = request.POST["year"]
        year_obj = Year.objects.get(year=year)
        c.y_id = year_obj
        c.save()
        request.session["name"]=name
        request.session["email"]=email
        return HttpResponse('success')
    else:
        return HttpResponse('error');


def web_upload_resume(request):
    # sanika account
    # Lae_eeDcmDgAAAAAAAACpAf6K4pN2cMT9Pa3UcARF6HVT5kbljzzyo7DazeUtE9D

    # Sirs account
    dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')
    st = dbx.users_get_current_account()


    email = request.session['email']
    print email
    student = Student.objects.get(email=email)
    roll = student.roll
    if request.FILES["resume"]:
        myfile = request.FILES["resume"]
        data = myfile.read()
        filename = myfile.name
        extension = filename.split('.')
        file_to = "/students/" + str(roll) + '.' + extension[1]
        print file_to
        dbx.files_upload(data, file_to)

        url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

        payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
        print payload
    # Sanika account
    # Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR
    # Sirs account
        headers = {
            'authorization': "Bearer 39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi",
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        res = json.loads(response.text)
        url = res["url"]
        student.url = url
        student.save()
        name = request.session["name"]
        return render(request, 'app/home.html', {"login": 2, "name": name})
    else:
        HttpResponse("Error")

@csrf_exempt
def web_login(request):
    if request.method == "POST":
        print "in web_login"
        get_mail = request.POST.get("email")
        get_pw = request.POST.get("password")
        print (get_mail)

        if Student.objects.filter(email=get_mail).exists():
            obj = Student.objects.get(email=get_mail)
            if obj.placed:
                return HttpResponse("You can't login since you are placed.")
            if obj.password == get_pw:
                name = obj.name
                print name, get_mail
                request.session['email'] = get_mail
                request.session['name'] = name
                return HttpResponse("Success")
            else:
                return HttpResponse("Incorrect Password")

        elif Admin.objects.filter(email=get_mail).exists():
            obj = Admin.objects.get(email=get_mail)
            if obj.password == get_pw:
                name = obj.name
                request.session['email'] = get_mail
                request.session['name'] = name
                return HttpResponse("Success")
            else:
                return HttpResponse("Incorrect Password")

        else:
            return HttpResponse("User not found")

@csrf_exempt
def web_apply_company(request):
    email = request.session["email"]
    student =  Student.objects.get(email=email)
    c_id = int(request.POST["c_id"])
    company = Company.objects.get(c_id=c_id)
    if student.placed:
        return  HttpResponse("You are already placed.")
    if not student.lock:
        return  HttpResponse("Can't apply unless your profile is verified.")
    if company.reg_end == None:
        return HttpResponse("Not accepting applications")
    back_allowed = company.back
    applied = request.POST["applied"]
    print "Already applied " ,applied    
    reg_end = company.reg_end
    if applied == "false":
        if reg_end and timezone.now()>reg_end:
            print "deadline over"
            return HttpResponse("Already Applied.Deadline over.")
        company.applied_students.remove(student)
        print company.applied_students.all()
        return HttpResponse("Removed Application Successfully")
    else:
        if reg_end and timezone.now()>reg_end:
            print "deadline over"
            return HttpResponse("Can't Apply. Deadline over.")
        else: 
            if company.back == "Active not Allowed" and student.active_back > 0:
                return HttpResponse("Can't apply. Active not Allowed")
            elif company.back == "Passive not Allowed" and student.passive_back:
                return HttpResponse("Can't apply. Passive back not allowed")
            elif(student.average<=company.criteria):
                return HttpResponse("Can't apply. Your average is below criteria.")
            else:
                company.applied_students.add(student)
                return HttpResponse("Applied Successfully")
    
@csrf_exempt
def web_edit_profile(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        roll = request.POST["roll"]
        print name, email
        c = Student.objects.get(email=email)
        c.name = name
        c.email = email
        c.gender = request.POST["gender"]
        c.roll = roll
        c.college_id = request.POST["college_id"]
        c.phone = request.POST["phone"]
        c.branch = request.POST["branch"]
        year = request.POST["year"]
        c.prn = request.POST["prn"]
        year_obj = Year.objects.get(year=year)
        c.y_id = year_obj
        c.save()
        request.session["name"]=name
        request.session["email"]=email
        return HttpResponse('success')
    else:
        return HttpResponse('error');


@csrf_exempt
def web_edit_ssc_marks(request):
    if request.method == "POST":
        email = request.session["email"]
        obj  =Student.objects.get(email=email)
        obj.tenth_board  = request.POST["tenth_board"]

        tenth_marks = request.POST["tenth_marks"]
        if tenth_marks:
            obj.tenth_marks = tenth_marks
        obj.tenth_schoolname  = request.POST["tenth_schoolname"]
        obj.tenth_city  = request.POST["tenth_city"]
        
        list_checked = request.POST.getlist("tenth_yeargap")
        list_checked = list(list_checked)
        print list_checked
        if "tenth_yeargap" in list_checked:
            obj.tenth_yeargap = True
            obj.tenth_yeargap_reason  = request.POST["tenth_yeargap_reason"]
        else:
            obj.tenth_yeargap = False

        list_checked = request.POST.getlist("is_diploma")
        list_checked = list(list_checked)
        print list_checked
        if "is_diploma" in list_checked:
            obj.is_diploma = True
           
        else:
            obj.is_diploma= False

        
    
        obj.save()        
        return HttpResponse('success');

@csrf_exempt
def web_edit_hsc_marks(request):
    if request.method == "POST":
        email = request.session["email"]
        obj  =Student.objects.get(email=email)

        if not obj.is_diploma:
            obj.twelveth_board  = request.POST["twelveth_board"]
            obj.twelveth_year  = request.POST["twelveth_year"]

            twelveth_marks = request.POST["twelveth_marks"]
            if twelveth_marks:
                obj.twelveth_marks = twelveth_marks

            obj.twelveth_schoolname  = request.POST["twelveth_schoolname"]
            obj.twelveth_city  = request.POST["twelveth_city"]

            list_checked = request.POST.getlist("twelveth_yeargap")
            list_checked = list(list_checked)
          
            if "twelveth_yeargap" in list_checked:
                obj.twelveth_yeargap = True
                obj.twelveth_yeargap_reason  = request.POST["twelveth_yeargap_reason"]
            else:
                obj.twelveth_yeargap = False
        else:
            obj.diploma_board = request.POST["diploma_board"]
            obj.diploma_marks = request.POST["diploma_marks"]
            obj.diploma_outof  = request.POST["diploma_outof"]
            obj.diploma_year  =  request.POST["diploma_year"]
        obj.save()

        return HttpResponse("success")

@csrf_exempt
def web_edit_be_marks(request):
    if request.method == "POST":
        email = request.session["email"]
        obj  =  Student.objects.get(email=email)

        if not obj.is_diploma:
            obj.fe_marks = request.POST["fe_marks"]
            obj.fe_outof = request.POST["fe_outof"]
        
        obj.se_marks = request.POST["se_marks"]
        obj.se_outof = request.POST["se_outof"]
        
        obj.te_marks = request.POST["te_marks"]
        obj.te_outof = request.POST["te_outof"]
        
        obj.total_marks = request.POST["total_marks"]
        obj.total_outof = request.POST["total_outof"]
        
        obj.average = request.POST["average"]
        obj.active_back = request.POST["active_back"]

        list_checked = request.POST.getlist("passive_back")
        list_checked = list(list_checked)
       
        if "passive_back" in list_checked:
            obj.passive_back = True
        else:
            obj.passive_back = False

        list_checked = request.POST.getlist("be_yeargap")
        list_checked = list(list_checked)
       
        if "be_yeargap" in list_checked:
            obj.be_yeargap = True
        else:
            obj.be_yeargap = False

        obj.save()
        return HttpResponse("success")


@csrf_exempt
def web_edit_other_details(request):
    if request.method == "POST":
        email = request.session["email"]
        obj  =  Student.objects.get(email=email)
        obj.birth_date  = request.POST["birth_date"]

        obj.aadhar_number = request.POST["aadhar_number"]
        obj.pan_number = request.POST["pan_number"]
        obj.passport_number = request.POST["passport_number"]
        obj.cur_address = request.POST["cur_address"]
        obj.per_address = request.POST["per_address"]
        obj.city = request.POST["city"]  
        obj.save()
      
        return HttpResponse("success")


@csrf_exempt
def web_change_password(request):
    if request.method == "POST":
        email  =request.session["email"]
        student = Student.objects.get(email=email)
        password = student.password
        old_password = request.POST["old_password"]
        if old_password != password:
            return HttpResponse("wrong")
        else:
            student.password = request.POST["new_password"]
        student.save()
        return HttpResponse("success")



#######UPLOAD ADMIN  ###################
########################################
########################################


@csrf_exempt
def web_lock_student(request):
    if request.method == "POST":
        prn = request.POST["prn"]
        student = Student.objects.get(prn=prn)
        
        student.lock = 1
        student.save()
        return HttpResponse("success")

@csrf_exempt
def web_unlock_student(request):
    if request.method == "POST":
        prn = request.POST["prn"]
        student = Student.objects.get(prn=prn)
        
        if student.lock == 1:
            student.lock = 0
            student.save()
        return HttpResponse("success")


@csrf_exempt
def web_verify(request):
    if request.method == "POST":
        prn = request.POST["prn"]
        if Verify.objects.filter(prn=prn).exists():
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")



@csrf_exempt
def web_register_company(request):
    if request.method == "POST":
        year = request.POST["year"]
        name = request.POST["name"]
        salary = request.POST["salary"]
        position = request.POST["position"]
        criteria = request.POST["criteria"]
        back = request.POST["back"]
        ppt_date = request.POST["ppt_date"]
        ppt_time = request.POST["ppt_time"]
        other_details = request.POST["other_details"]
        reg_end_date = request.POST["reg_end_date"]
        reg_end_time = request.POST["reg_end_time"]



        if ppt_date:
            ppt_date = str(ppt_date)
            print (ppt_date)

            ppt_date = datetime.datetime.strptime(ppt_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            print (ppt_date)

        if reg_end_date:
            reg_end_date = datetime.datetime.strptime(reg_end_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            reg_end = reg_end_date + " " + reg_end_time
            
        else:
            reg_end = None


        if other_details == "":
            other_details = None
            # add to database

        year_obj = Year.objects.get(year=year)

        obj = Company()
        obj.name = name
        obj.y_id = year_obj

        if criteria:
            obj.criteria = criteria
        if salary:
            obj.salary = salary
        if position:
            obj.position = position
        if other_details:
            obj.other_details = other_details
        if ppt_date:
            obj.ppt_date = ppt_date + " " + ppt_time
        if reg_end:
            obj.reg_end = reg_end
        if back:
            obj.back = back


        codes = Company.objects.values('code_name')
        print codes
        while(1):
            s = string.lowercase + string.digits
            code = ''.join(random.sample(s, 4))
            if code not in codes:
                obj.code_name = code
                obj.save()
                break

        # send notification
        Device = get_device_model()
        c_id = obj.c_id;
        Device.objects.all().send_message({'type': 'company_reg', 'c_id':c_id,'name': name, 'criteria': criteria,'position':position, 'salary': salary,
                                           'other_details': other_details, 'ppt_date': ppt_date,'reg_end': reg_end, 'back': back})
        print ("Success")
        return HttpResponse("success")
    else:
        return HttpResponse("error")


@csrf_exempt
def web_update_company(request):
    if request.method == "POST":
        name = request.POST["name"]
        print (name)

        year = Year.objects.order_by('-y_id')[0]
        obj = Company.objects.get(name=name, y_id=year)

        reg_link = request.POST["reg_link"]
        obj.reg_link = reg_link

        reg_start_date = request.POST["reg_start_date"]
        reg_start_time = request.POST["reg_start_time"]

        reg_end_date = request.POST["reg_end_date"]
        reg_end_time = request.POST["reg_end_time"]

        # convert dateformat

        if reg_start_date:
            reg_start_date = datetime.datetime.strptime(reg_start_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            reg_start = reg_start_date + " " + reg_start_time
            obj.reg_start = reg_start

        else:
            reg_start = None

        if reg_end_date:
            reg_end_date = datetime.datetime.strptime(reg_end_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            reg_end = reg_end_date + " " + reg_end_time
            obj.reg_end = reg_end
        else:
            reg_end = None

        other_details = request.POST["other_details"]

        if obj.other_details and other_details:
            obj.other_details = obj.other_details + " " + other_details
        elif other_details:
            obj.other_details = other_details
        obj.save()
        c_id = obj.c_id;
        # send notifications
        Device = get_device_model()
        Device.objects.all().send_message(
            {'type': 'company_update', 'c_id':c_id,'name': name, 'reg_link': reg_link, 'reg_start': reg_start, 'reg_end': reg_end,
             'other_details': other_details})

        return HttpResponse("success")
    return HttpResponse("error")

@csrf_exempt
def web_edit_company(request):
    if request.method == "POST":
        name = request.POST["name"] #gives id
        year = Year.objects.order_by('-y_id')[0]
        obj = Company.objects.get(c_id=name, y_id=year) #name contains id
        c_id = obj.c_id
        salary = request.POST["salary"]
        criteria = request.POST["criteria"]
        position = request.POST["position"]
        if "back" in request.POST:
            back = request.POST["back"]
        else:
            back = None
        ppt_date = request.POST["ppt_date"]
        ppt_time = request.POST["ppt_time"]

        if criteria:
            obj.criteria = criteria
        if salary:
            obj.salary = salary
        if position:
            obj.position=position
        if ppt_date:
            obj.ppt_date = ppt_date + " " + ppt_time
        if back:
            obj.back = back

        if len(str(ppt_date))>1:
            ppt_date = str(ppt_date)

            obj.ppt_date = datetime.datetime.strptime(ppt_date, '%m/%d/%Y').strftime('%Y-%m-%d') +" " + ppt_time
            print  obj.ppt_date + "in if"
        else:
            ppt_date = None
        print ppt_date
        # reg_link = request.POST["reg_link"]
        # reg_start_date = request.POST["reg_start_date"]
        # reg_start_time = request.POST["reg_start_time"]
        # # convert date format
        # if reg_start_date :
        #     reg_start_date = datetime.datetime.strptime(reg_start_date, '%m/%d/%Y').strftime('%Y-%m-%d')

        reg_end_date = request.POST["reg_end_date"]
        reg_end_time = request.POST["reg_end_time"]
        # convert dateformat
        if reg_end_date:
            reg_end_date = datetime.datetime.strptime(reg_end_date, '%m/%d/%Y').strftime('%Y-%m-%d')

        other_details = request.POST["other_details"]
        hired_count = request.POST["hired_count"]

        # reg_start = reg_start_date + " " + reg_start_time
        reg_end = reg_end_date + " " + reg_end_time


        # if len(str(reg_start))>1:
        #     obj.reg_start = reg_start
        # else:
        #     reg_start = None

        if len(str(reg_end))>1:
            obj.reg_end = reg_end
        else:
            reg_end = None

        # if len(str(reg_link)) > 1:
        #     obj.reg_link = reg_link
        # else:
        #     reg_link = None

        if hired_count:
            obj.hired_count = hired_count
        else:
            hired_count=0

        if obj.other_details and other_details:
            obj.other_details = obj.other_details + " " + other_details
        elif other_details:
            obj.other_details = other_details
        else:
            other_details= None

        obj.save()
        # c_id = obj.c_id
        # send notification
        Device = get_device_model()

        Device.objects.all().send_message(
            {'type': 'company_edit', 'c_id': c_id, 'name': name, 'criteria': criteria, 'salary': salary,
             'position':position,'other_details': other_details, 'ppt_date': ppt_date, 'back': back,
             'reg_end': reg_end,  'hired_count': hired_count})

        print ("Success")
        return HttpResponse("success")
    else:
        return HttpResponse("error")


@csrf_exempt
def web_notify(request):
    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        obj = Message()
        obj.title = title
        obj.message = body
        obj.timestamp = datetime.datetime.now()
        obj.save()
        if len(request.FILES) != 0:
            if request.FILES["file"]:
                # sanika account
                # Lae_eeDcmDgAAAAAAAACpAf6K4pN2cMT9Pa3UcARF6HVT5kbljzzyo7DazeUtE9D

                # Sirs account
                dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')
                st = dbx.users_get_current_account()


                myfile = request.FILES["file"]
                data = myfile.read()
                filename = myfile.name
                extension = filename.split('.')
                file_to = "/messages/" + title + '.' + extension[1]
                print file_to
                dbx.files_upload(data, file_to)

                url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

                payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
                print payload
                # sanika account
                # Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR
                #Sirs account
                headers = {
                    'authorization': "Bearer 39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi",
                    'content-type': "application/json",
                    'cache-control': "no-cache",
                }

                response = requests.request("POST", url, data=payload, headers=headers)

                res = json.loads(response.text)
                url = res["url"]
                obj.url = url
                obj.save()

                body = body + "\n" + url
        Device = get_device_model()
        Device.objects.all().send_message({'type': 'gen_msg', 'title': title, 'body': body})
        name = request.session["name"]
        return render(request, 'app/home.html', {"name": name, "login": 1})
    else:
        return HttpResponse("error")


@csrf_exempt
def web_upload_result(request):
    if request.method == "POST":
        choice = request.POST["choice"]
        c_id = request.POST["company"]
        company = Company.objects.get(c_id=c_id)
        if request.FILES["resultfile"]:
            # sanika account
            # Lae_eeDcmDgAAAAAAAACpAf6K4pN2cMT9Pa3UcARF6HVT5kbljzzyo7DazeUtE9D

            # Sirs account
            dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')
            st = dbx.users_get_current_account()


            myfile = request.FILES["resultfile"]
            data = myfile.read()
            filename = myfile.name
            extension = filename.split('.')
            filename = company.name + ' ' + choice + '.' + extension[1]
            file_to = "/results/" + filename
            print file_to
            dbx.files_upload(data, file_to)

            url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

            payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
            print payload
            # Sanikas account
            # Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR
            # Sirs account
            headers = {
                'authorization': "Bearer 39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi",
                'content-type': "application/json",
                'cache-control': "no-cache",
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            res = json.loads(response.text)
            url = res["url"]

            # store in table
            obj = Result()

            obj.c_id = company
            obj.shortlist = choice
            obj.filename = filename
            obj.url = url

            if "other_details" in request.POST:
                obj.other_details = request.POST["other_details"]
            obj.save()

            # save the url in company table
            if choice == "Placed":
                company.placed_url = url
                company.save()

            title = company.name + " " + choice

            Device = get_device_model()
            Device.objects.all().send_message({'type': 'result', 'title': title, 'url': url})
            name = request.session["name"]
            return render(request, 'app/home.html', {"login": 1, "name": name})
        else:
            HttpResponse('file')
    else:
        HttpResponse('error')

@csrf_exempt
def web_placed_students(request):
    c_id = request.POST["c_id"]
    company = Company.objects.get(c_id=c_id)

    studentsList = company.student_set.all()
    if company.lock == 0:
        for student in studentsList:
            student.placed= False
            student.c_id = None
            student.save()

        print request.POST
        students = request.POST["placed_arr"]
        students = json.loads(students)

        for i in students:
            i = int(i)
            student = Student.objects.get(s_id=i)
            student.c_id = company
            student.placed = True
            student.save()

        hired_count = len(students)
        company.hired_count = hired_count
        company.save()

        return HttpResponse(""+ str(hired_count) + " Students added Successfully to " +company.name)
    else:
        return  HttpResponse("Company Locked")

@csrf_exempt
def web_lock_company(request):
    c_id = request.POST["c_id"]
    company = Company.objects.get(c_id=c_id)
    company.lock = 1
    company.status = "Closed"
    company.save()
    return HttpResponse(company.name + " Locked Successfully")


@csrf_exempt
def web_hide_company(request,cid):
    company = Company.objects.get(c_id=cid)
    if company.hidden:
        company.hidden = 0
        company.save()
        return HttpResponse(company.name + " Company will be visible to students now.")
    else:
        company.hidden = 1
        company.save()
        return HttpResponse(company.name + " Company won't be visible to students now.")


#########called from ajax######
@csrf_exempt
def web_download_students(request):
    year = request.POST["year"]
    branch = request.POST["branch"]
    minavg = request.POST["minavg"]
    maxavg = request.POST["maxavg"]

    if year == "All":
        students_year = Student.objects.all()

    else:
        year = Year.objects.get(year=year)
        students_year = Student.objects.filter(y_id=year)
        year = year.year

    if branch == "All":
        students_branch = students_year
    else:
        students_branch = students_year.filter(branch=branch)

    students_min_average = students_branch.filter(average__gte=minavg)

    students_max_average = students_min_average.filter(average__lte=maxavg)
    print students_max_average
    students = students_max_average

    with open('test.csv', 'w') as csv_file:
        write_csv(students, csv_file)

    data = open('test.csv', 'r').read()

    dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')

    filename = year  + " " +  branch  + " "  + maxavg + " " + minavg + ".csv"

    file_to = "/students/" + filename
    print file_to
    dbx.files_upload(data, file_to)

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

    payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
    print payload

    # Sanikas account
    # Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR
    # Sirs account
    headers = {
        'authorization': "Bearer 39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi",
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    res = json.loads(response.text)
    url = res["url"]
    print  url
    return render_to_csv_response(students)


@csrf_exempt
def web_download_companies(request):
    minsal = request.POST["minsal"]
    maxsal = request.POST["maxsal"]
    mincri = request.POST["mincri"]
    maxcri = request.POST["maxcri"]

    companies_min_salary = Company.objects.filter(salary__gte = minsal)
    companies_max_salary = companies_min_salary.filter(salary__lte = maxsal)
    companies_min_criteria = companies_max_salary.filter(criteria__gte = mincri)
    companies_max_criteria = companies_min_criteria.filter(criteria__lte = maxcri)

    companies = companies_max_criteria

    filename = minsal + "to" + maxsal + "lpa_" + mincri + "to" + maxcri + "criteria.csv"
    with open('test.csv', 'w') as csv_file:
        write_csv(companies, csv_file)

    data = open('test.csv', 'r').read()
    dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')
    file_to = "/companies/" + filename

    print file_to
    dbx.files_upload(data, file_to)

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

    payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
    print payload
    # Sanikas account
    # Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR
    # Sirs account
    headers = {
        'authorization': "Bearer 39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi",
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    res = json.loads(response.text)
    url = res["url"]
    print  url
    return render_to_csv_response(companies)


@csrf_exempt
def web_download_applied_students(request):
    c_id  = request.POST["c_id"]
    company = Company.objects.get(c_id=c_id)
    applied_students = company.applied_students.all()

    filename = company.name  + "_applied_students list.csv"
    with open('test.csv', 'w') as csv_file:
        write_csv(applied_students, csv_file)

    data = open('test.csv', 'r').read()
    dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')
    file_to = "/appliedstudents/" + filename

    print file_to
    dbx.files_upload(data, file_to)

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

    payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
    print payload
    # Sanikas account
    # Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR
    # Sirs account
    headers = {
        'authorization': "Bearer 39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi",
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    res = json.loads(response.text)
    url = res["url"]
    print  url
    return render_to_csv_response(applied_students)
