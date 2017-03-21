from django.shortcuts import render
from .models import Student, Company, Message, Verify, Result, Admin ,Year , Average
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from django.template.loader import render_to_string
from django.views.decorators.csrf import *
from django.core import serializers
from gcm.models import get_device_model
import json,csv
import dropbox
import requests

dbx = dropbox.Dropbox('Lae_eeDcmDgAAAAAAAACpAf6K4pN2cMT9Pa3UcARF6HVT5kbljzzyo7DazeUtE9D')
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
    if Student.objects.filter(email=get_mail).exists():
        obj = Student.objects.get(email=get_mail)
        if obj.password == get_pw:
            return HttpResponse(obj.name)
        else:
            return HttpResponse("Incorrect Password")
    else:
        return HttpResponse("User not found")


@csrf_exempt
def register_company(request):
    data = json.loads(request.body)
    name = data["name"]
    if (Company.objects.filter(name=name).exists()):
        return HttpResponse("Already Registered")

    criteria = data["criteria"]
    salary = data["salary"]
    other_details = data["other_details"]
    ppt_date = data["ppt_date"]
    back = data["back"]

    # add to database
    obj = Company()
    obj.name = name
    obj.criteria = criteria
    obj.salary = salary
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
    if obj.reg_link:
        return HttpResponse("Already Updated")
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


###WEB###
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
def get_signup_page(request):
    years = list(Year.objects.all().order_by('-y_id'))
    print ("hello")
    return render(request, 'app/signup.html', {"years":years})


@csrf_exempt
def get_login_page(request):
    print "in login page"
    return render(request, 'app/login.html', {})


#####UPLOAD pages
@csrf_exempt
def get_register_page(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            return render(request, 'app/companyRegister.html', {"name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")

@csrf_exempt
def get_update_page(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            companies = list(Company.objects.all().order_by('-c_id'))
            return render(request, 'app/update.html', {"companies": companies, "name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")


@csrf_exempt
def get_notify_page(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
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
        return render(request, 'app/login.html', {})
    else:
        get_mail = request.session["email"]
        if Admin.objects.filter(email=get_mail).exists():
            name = request.session["name"]
            companies = list(Company.objects.all().order_by('-c_id'))
            return render(request, 'app/resultUpload.html', {"companies": companies, "name": name})

        # student login
        else:
            return HttpResponse("Not permitted to access")


#######DISPLAY Pages######

@csrf_exempt
def get_students_page(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
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
            averages = Average.objects.all()
            name = request.session["name"]
            return render(request, 'app/students.html', {"students": students, "years":years ,"year":year,"branch":branch,"minavg":minavg,"maxavg":maxavg,"name": name})
        # student login
        else:
            return HttpResponse("Not permitted to access")

#handled using ajax
@csrf_exempt
def get_student_page(request, roll):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
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
        return render(request, 'app/login.html', {})
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
def get_statistics_page(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
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

        ##min salary
        if "minsal" in request.POST:
            minsal = request.POST["minsal"]
            companies_min_salary = Company.objects.filter(salary__gte=minsal)
        else:
            companies_min_salary = Company.objects.all().order_by('-c_id')


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

        companies = companies_max_criteria.order_by('-c_id')

        name = request.session["name"]
        
        return render(request, 'app/statistics.html', {"companies": companies,"minsal":minsal ,"maxsal":maxsal,"mincri":mincri, "maxcri":maxcri ,"name": name, "login": login})


@csrf_exempt
def get_results_page(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
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
        return render(request, 'app/results.html', {"results": results, "name": name, "login": login})


@csrf_exempt
def get_company_page(request, cid):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
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
            return render(request, 'app/company.html', {"company": company, "name": name, "login": login})
        else:
            return HttpResponse("Not Found")

@csrf_exempt
def logout(request):
    if not request.session.get("name"):
        return render(request, 'app/login.html', {})
    else:

        del request.session['email']
        del request.session['name']
        request.session.modified = True
        print "end"
        return render(request, 'app/redirect2.html', {})



#####upload#####
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
        c.phone = request.POST["phone"]
        c.year = request.POST["year"]
        c.branch = request.POST["branch"]
        c.ssc = request.POST["10th"]
        c.hsc = request.POST["12th"]
        c.average = request.POST["average"]

        # c.activeBack=request.POST.get("activeBack")

        # for entry in dbx.files_list_folder('').entries:
        #   print(entry.name)
        if request.FILES["resume"]:
            myfile = request.FILES["resume"]
            data = myfile.read()
            filename = myfile.name
            extension = filename.split('.')
            file_to = "/students/" + roll + '.' + extension[1]
            print file_to
            dbx.files_upload(data, file_to)

            url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

            payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
            print payload
            headers = {
                'authorization': "Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR",
                'content-type': "application/json",
                'cache-control': "no-cache",
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            res = json.loads(response.text)
            url = res["url"]
            c.url = url
            c.save()

        return render(request, 'app/login.html', {})
    else:
        return HttpResponse('Error');


@csrf_exempt
def web_login(request):
    if request.method == "POST":
        print "in web_login"
        get_mail = request.POST.get("email")
        get_pw = request.POST.get("password")
        print (get_mail)
        if Admin.objects.filter(email=get_mail).exists():
            obj = Admin.objects.get(email=get_mail)
            if obj.password == get_pw:
                name = obj.name
                request.session['email'] = get_mail
                request.session['name'] = name
                return HttpResponse("Success")
            else:
                return HttpResponse("Incorrect Password")

        elif Student.objects.filter(email=get_mail).exists():
            obj = Student.objects.get(email=get_mail)
            if obj.password == get_pw:
                name = obj.name
                print name, get_mail
                request.session['email'] = get_mail
                request.session['name'] = name
                return HttpResponse("Success")
            else:
                return HttpResponse("Incorrect Password")

        else:
            return HttpResponse("User not found")


@csrf_exempt
def web_verify(request):
    if request.method == "POST":
        prn = request.POST["prn"]
        if Verify.objects.filter(prn=prn).exists():
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")

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
                file_to = "/Messages/" + title + '.' + extension[1]
                print file_to
                dbx.files_upload(data, file_to)

                url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

                payload = "{\"path\":" + '"' + file_to + '"' + ",\"short_url\": true}"
                print payload
                headers = {
                    'authorization': "Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR",
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
            headers = {
                'authorization': "Bearer Lae_eeDcmDgAAAAAAAACpcij58JNKKidOEQRTOx56qvE7hUiOJs_QW75We_r1psR",
                'content-type': "application/json",
                'cache-control': "no-cache",
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            res = json.loads(response.text)
            url = res["url"]

            # store in table
            obj = Result()
            obj.company = company
            obj.shortlist = choice
            obj.filename = filename
            obj.url = url
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

@csrf_exempt
def web_register_company(request):
    if request.method == "POST":
        name = request.POST["name"]
        if Company.objects.filter(name=name).exists():
            return HttpResponse('exists')
        name = request.POST["name"]
        salary = request.POST["salary"]
        criteria = request.POST["criteria"]
        back = request.POST["back"]
        ppt_date = request.POST["ppt_date"]
        ppt_time = request.POST["ppt_time"]
        other_details = request.POST["other_details"]
        if other_details == "":
            other_details = None
            # add to database
        obj = Company()
        obj.name = name
        obj.criteria = criteria
        obj.salary = salary
        obj.other_details = other_details
        obj.ppt_date = ppt_date + " " + ppt_time
        obj.back = back
        obj.save()

        # send notification
        Device = get_device_model()

        Device.objects.all().send_message({'type': 'company_reg', 'name': name, 'criteria': criteria, 'salary': salary,
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
        reg_link = request.POST["regLink"]
        reg_start_date = request.POST["regStartDate"]
        reg_start_time = request.POST["regStartTime"]
        reg_end_date = request.POST["regEndDate"]
        reg_end_time = request.POST["regEndTime"]
        other_details = request.POST["otherDetails"]
        obj = Company.objects.get(name=name)
        if obj.reg_link:
            return HttpResponse("updated")
        reg_start = reg_start_date + " " + reg_start_time
        reg_end = reg_end_date + " " + reg_end_time
        print (reg_start, reg_end)
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

        return HttpResponse("success")
    return HttpResponse("error")

