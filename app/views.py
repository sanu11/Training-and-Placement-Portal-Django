import datetime
from django.shortcuts import render
from .models import Student, Company, Message, Verify, Result, Admin ,Year
from django.http import HttpResponse
from django.views.decorators.csrf import *
from django.core import serializers
from gcm.models import get_device_model
import json,csv
import dropbox
import requests
# sanika account
# Lae_eeDcmDgAAAAAAAACpAf6K4pN2cMT9Pa3UcARF6HVT5kbljzzyo7DazeUtE9D

# Sirs account
dbx = dropbox.Dropbox('39HKzewZZ6AAAAAAAAAADYTBmHhTrhWOgP_4VMABOZOyezxh5G35921KEGPSIwsi')
st = dbx.users_get_current_account()


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
    if Student.oeeebjects.filter(email=get_mail).exists():
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
        name = request.session["name"]
        get_mail = request.session["email"]
        # admin login
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"

        return render(request, 'app/home.html', {"login": login, "name": name})


@csrf_exempt
def get_developers_page(request):
    if  request.session.get("name"):
        name = request.session["name"]
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            login = 1
            print "Admin login"
            name = request.session["name"]
        
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
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
            companies = list(Company.objects.all().order_by('-c_id'))
            return render(request, 'app/resultUpload.html', {"companies": companies, "name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")

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
            a_id = "All"
            if  "year"  in request.POST:
                year = request.POST["year"]
                if not year == "All":
                    students_year = Student.objects.filter(year=year)
                else:
                    students_year = Student.objects.all()
            else:
                students_year = Student.objects.all()

            if  "branch" in request.POST:
                branch = request.POST["branch"]
                if not branch == "All":
                    students_branch = students_year.filter(branch=branch)
                else:
                    students_branch = students_year
            else:
                students_branch = students_year

            minavg = 0
            maxavg=100
            
            if "minavg" in request.POST:
                minavg = request.POST["minavg"]
                students_min_average = students_branch.filter(average__gte =minavg)
            else:
                students_min_average = students_branch

            if "maxavg" in request.POST:
                maxavg = request.POST["maxavg"]
                students_max_average = students_min_average.filter(average__lte= maxavg)
            else:
                students_max_average = students_min_average

            students = students_max_average
            years = Year.objects.all().order_by('-y_id')
           
            name = request.session["name"]
            return render(request, 'app/students.html', {"students": students, "years":years ,"year":year,"branch":branch,"minavg":minavg,"maxavg":maxavg,"name": name})
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
                return render(request, 'app/student.html', {"student": student, "name": name})
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
        # student login
        elif Student.objects.filter(email=get_mail).exists():
            login = 2
            print "Student login"
        name = request.session["name"]
        notifications = Message.objects.all().order_by('-msg_id')
        return render(request, 'app/notification.html', {"notifications": notifications, "name": name, "login": login})


@csrf_exempt
def get_companies_page(request):
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
        minsal = 0
        maxsal = 50
        mincri = 0
        maxcri = 100


        #year
        if "year" in request.POST:
            year = request.POST["year"]
            year_obj = Year.objects.get(year=year)
        else:
            year_obj = Year.objects.order_by('-y_id')[0]

        companies_year = Company.objects.filter(y_id=year_obj)

        ##min salary
        if "minsal" in request.POST:
            minsal = request.POST["minsal"]
            companies_min_salary =companies_year.filter(salary__gte=minsal)
        else:
            companies_min_salary = companies_year

        ##max salary
        if "maxsal" in request.POST:
            maxsal = request.POST["maxsal"]
            companies_max_salary = companies_min_salary.filter(salary__lte=maxsal)
        else:
            companies_max_salary = companies_min_salary

        ##min criteria
        if "mincri" in request.POST:
            mincri = request.POST["mincri"]
            companies_min_criteria = companies_max_salary.filter(criteria__gte=mincri)
        else:
            companies_min_criteria = companies_max_salary

        ##max cri
        if "maxcri" in request.POST:
            maxcri = request.POST["maxcri"]
            print maxcri
            companies_max_criteria = companies_min_criteria.filter(criteria__lte=maxcri)
            print companies_max_criteria
        else:
            companies_max_criteria = companies_min_criteria

        companies = companies_max_criteria.order_by('ppt_date')
        years = Year.objects.all()
        name = request.session["name"]
        curr_year = Year.objects.order_by('-y_id')[0]
        return render(request, 'app/companies.html', {"companies": companies,"years":years,"curr_year":curr_year,"minsal":minsal ,"maxsal":maxsal,"mincri":mincri, "maxcri":maxcri ,"name": name, "login": login})


@csrf_exempt
def get_results_page(request):
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
        results = Result.objects.all().order_by('-r_id')
        print results
        return render(request, 'app/resultsDisplay.html', {"results": results, "name": name, "login": login})


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

        if ppt_date:
            ppt_date = str(ppt_date)
            print (ppt_date)

            ppt_date = datetime.datetime.strptime(ppt_date, '%m/%d/%Y').strftime('%Y-%m-%d')
            print (ppt_date)

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
        if back:
            obj.back = back
        obj.save()

        # send notification
        Device = get_device_model()
        c_id = obj.c_id;
        Device.objects.all().send_message({'type': 'company_reg', 'c_id':c_id,'name': name, 'criteria': criteria,'position':position, 'salary': salary,
                                           'other_details': other_details, 'ppt_date': ppt_date, 'back': back})
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
        reg_link = request.POST["reg_link"]
        reg_start_date = request.POST["reg_start_date"]
        reg_start_time = request.POST["reg_start_time"]
        # convert date format
        if reg_start_date :
            reg_start_date = datetime.datetime.strptime(reg_start_date, '%m/%d/%Y').strftime('%Y-%m-%d')

        reg_end_date = request.POST["reg_end_date"]
        reg_end_time = request.POST["reg_end_time"]
        # convert dateformat
        if reg_end_date:
            reg_end_date = datetime.datetime.strptime(reg_end_date, '%m/%d/%Y').strftime('%Y-%m-%d')

        other_details = request.POST["other_details"]
        hired_count = request.POST["hired_count"]

        reg_start = reg_start_date + " " + reg_start_time
        reg_end = reg_end_date + " " + reg_end_time


        if len(str(reg_start))>1:
            obj.reg_start = reg_start
        else:
            reg_start = None

        if len(str(reg_end))>1:
            obj.reg_end = reg_end
        else:
            reg_end = None

        if len(str(reg_link)) > 1:
            obj.reg_link = reg_link
        else:
            reg_link = None

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
             'reg_start':reg_start,'reg_end': reg_end, 'reg_link': reg_link, 'hired_count': hired_count})

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
        obj.save()
        if len(request.FILES) != 0:
            if request.FILES["file"]:
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
        company = request.POST["company"]

        print choice
        if request.FILES["resultfile"]:
            myfile = request.FILES["resultfile"]
            data = myfile.read()
            filename = myfile.name
            extension = filename.split('.')
            filename = company + ' ' + choice + '.' + extension[1]
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

            obj.c_id = Company.objects.get(name=company)
            obj.shortlist = choice
            obj.filename = filename
            obj.url = url

            if "other_details" in request.POST:
                obj.other_details = request.POST["other_details"]
            obj.save()

            # save the url in company table
            if choice == "Placed":
                obj = Company.objects.get(name=company)
                obj.placed_url = url
                obj.save()

            title = company + " " + choice

            Device = get_device_model()
            Device.objects.all().send_message({'type': 'result', 'title': title, 'url': url})
            name = request.session["name"]
            return render(request, 'app/home.html', {"login": 1, "name": name})
        else:
            HttpResponse('file')
    else:
        HttpResponse('error')


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
        students_year = Student.objects.filter(year=year)

    if branch == "All":
        students_branch = students_year
    else:
        students_branch = students_year.filter(branch=branch)

    students_min_average = students_branch.filter(average__gte=minavg)


    students_max_average = students_min_average.filter(average__lte=maxavg)

    students = students_max_average
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sanika.csv"'
    writer = csv.writer(response)
    writer.writerow(['Roll Number', 'Name','Email','Phone','Gender','Branch','SSC','HSC', 'Average','Active back','Resume'])
    for x in students:
        writer.writerow([x.roll, x.name , x.email , x.phone , x.gender, x.branch ,x.ssc , x.hsc , x.average ,x.active_back , x.url])
        print writer
    return response

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
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sanika.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Salary','Criteria','Date','Placed_Url','Hired ','Other_Details'])
    for x in companies:
        writer.writerow([x.name,x.salary,x.criteria,x.ppt_date,x.placed_url,x.hired_people,x.other_details])
        print writer
    return response
