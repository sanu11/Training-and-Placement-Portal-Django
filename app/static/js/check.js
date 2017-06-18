
function signup() {
        console.log('signupform');
        var signupform = $('#' + 'signupform');
        var csrftoken = getCookie('csrftoken');
        var name = document.getElementById('name').value;
        var roll = document.getElementById('roll').value;
        var email = document.getElementById('email').value;
        var password  =document.getElementById('password').value;
        var phone = document.getElementById('phone').value;
       

        var atpos = email.indexOf("@");
        var dotpos = email.lastIndexOf(".");
        
        if(name.length==0 || roll.length==0 || email.length == 0 || password.length == 0 || phone.length == 0 )
            alert("Enter all Details"); 
        else if (roll.length !=4) 
            alert("Enter  valid 4 digit Roll number ");
    
        else if (atpos<1 || dotpos<atpos+2 || dotpos+2>=email.length) {
            alert("Enter valid e-mail address");
        
        }
        else if(password.length<6)
            alert("Password  should be greater than 5 digits")
        else if(phone.length!=10)
            alert ("Enter valid mobile number");
        
        else
        {
            $.ajax({
                type: "POST",
                url: '/signup/',
                data: signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       window.location.href = "/";
                    }
                    else if(message=='exists')
                        alert("User Exists.Please Login");
                    
                    else
                        alert('Error');
                    
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        }
    }   

function studentLogin() {
        console.log('loginform');
        var loginform = $('#' + 'loginform');
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            type: "POST",
            url: '/login/',
            data: loginform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
            success: function(message) {
            console.log(message);
                if (message =='Success') {
                   window.location.href = "/";
                }
                else if(message=='Incorrect Password')
                {
                    alert("Incorrect Password");
                }
                else if (message == 'User not found')
                {
                    alert('User not found');
                }
                else
                {
                alert('Error');
                }
            },
            error: function(xhr, errmsg, err) {
                alert('Error');
            },
        });
    }


function lock(prn){
        var csrftoken = getCookie('csrftoken');
        
        $.ajax({
            type: "POST",
            url: '/lockStudent/',
            data : {prn:prn,csrfmiddlewaretoken:csrftoken},
            success: function(message) {
            console.log(message);
                if (message =='success') {
                   window.location.href = "/psearch/";
                }
                else
                {
                alert('Error');
                }
            },
            error: function(xhr, errmsg, err) {
                alert('Error');
            },
        });
    }


function unlock(prn){
        var csrftoken = getCookie('csrftoken');
        var button1 = document.getElementById("lock1");
        var button2 = document.getElementById("lock2");
       
        $.ajax({
            type: "POST",
            url: '/unlockStudent/',
            data : {prn:prn,csrfmiddlewaretoken:csrftoken},
            success: function(message) {
            console.log(message);
                if (message =='success') {
                   alert("Unlocked Student");
                   button1.value = "Lock";
                   button2.value = "Lock";
                   location.reload();
                }
                else
                {
                alert('Error');
                }
            },
            error: function(xhr, errmsg, err) {
                alert('Error');
            },
        });
    }




    // function getStudentDetails() {

    //     var csrftoken = getCookie('csrftoken');
    //     var roll = document.getElementById("roll").value;
    //     var year = document.getElementById("year").value;

    //         $.ajax({
    //             type: "POST",
    //             url: '/roll/',
    //             data: {roll:roll,year:year,csrfmiddlewaretoken:csrftoken},
    //             success: function(message) {
    //             console.log(message);
    //             str  = jQuery.parseJSON(message);
    //             data = str[0]["fields"];

                

    //             },
    //             error: function(xhr, errmsg, err) {
    //                 alert('Error');
    //             },
    //         });

    // }



function editProfilePage(argument) {
    window.location.href = "/peditprofile";
    // body...
}

function editSscMarksPage(argument) {
    window.location.href = "/peditsscmarks";
    // body...
}
function editHscMarksPage(argument) {
    window.location.href = "/pedithscmarks";
    // body...
}

function editBeMarksPage(argument) {
    window.location.href = "/peditbemarks";
    // body...
}

function editOtherDetailsPage(argument) {
    window.location.href = "/peditotherdetails";
    // body...
}

function editProfile() {
        console.log('signupform');
        var signupform = $('#' + 'signupform');
        var csrftoken = getCookie('csrftoken');
        var name = document.getElementById('name').value;
        var roll = document.getElementById('roll').value;
        var email = document.getElementById('email').value;
        var phone = document.getElementById('phone').value;
       

        var atpos = email.indexOf("@");
        var dotpos = email.lastIndexOf(".");
        
        if (roll.length !=4)
            alert("Enter valid Roll number");
        else if (atpos<1 || dotpos<atpos+2 || dotpos+2>=email.length) {
            alert("Not a valid e-mail address");
        }
        else if(phone.length!=10)
            alert ("Enter Valid mobile number");
        
        else
        {
            $.ajax({
                type: "POST",
                url: '/editprofile/',
                data: signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       window.location.href = "/peditsscmarks/";
                    }
                    else
                    {
                    alert('Error');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        }
    }   

function editSscMarks() {
        console.log('signupform');
        var signupform = $('#' + 'signupform');
        var csrftoken = getCookie('csrftoken');
        var tenth_board = document.getElementById("tenth_board").value;
        var tenth_marks = document.getElementById("tenth_marks").value;       
        if (tenth_marks == "" || tenth_board == ""){
            alert("Please Enter 10th board and marks");
            return;
        }
            $.ajax({
                type: "POST",
                url: '/editsscmarks/',
                data: signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       window.location.href = "/pedithscmarks/";
                    }
                    else
                    {
                    alert('Error');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        
    }   


function editHscMarks(is_diploma) {
        console.log('signupform');
        var signupform = $('#' + 'signupform');
        var csrftoken = getCookie('csrftoken');
        if(!is_diploma){
        var twelveth_board = document.getElementById("twelveth_board").value;
        var twelveth_marks = document.getElementById("twelveth_marks").value;
        var twelveth_year = document.getElementById("twelveth_year").value;
               
        if (twelveth_marks == "" || twelveth_board == ""){
            alert("Please Enter All Details");
            return;
            }
        }
        else{
        var diploma_board = document.getElementById("diploma_board").value;
        var diploma_marks = document.getElementById("diploma_marks").value;
        var diploma_outof = document.getElementById("diploma_outof").value;
        var diploma_year = document.getElementById("diploma_year").value;
         
        if (diploma_marks == "" || diploma_board == "" || diploma_outof =="" || diploma_year==""){
            alert("Please Enter All Details");
            return;
            }
       
        }

    
            $.ajax({
                type: "POST",
                url: '/edithscmarks/',
                data: signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       window.location.href = "/peditbemarks/";
                    }
                    else
                    {
                    alert('Error');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        
    }   
    
function editBeMarks(is_diploma) {
        console.log('signupform');
        var signupform = $('#' + 'signupform');
        var csrftoken = getCookie('csrftoken');
        if(!is_diploma){
        var fe_marks  = document.getElementById("fe_marks").value;
        var fe_outof  = document.getElementById("fe_outof").value;
        if(fe_outof =="" ||fe_marks==""){
            alert("Enter FE marks");
        }

        }
        var se_marks = document.getElementById("se_marks").value;
        var se_outof = document.getElementById("se_outof").value;
        var te_marks = document.getElementById("te_marks").value;
        var te_outof = document.getElementById("te_outof").value;
        var total_marks = document.getElementById("total_marks").value;
        var total_outof = document.getElementById("total_outof").value;
        var average = document.getElementById("average").value;
        
        
        if(se_marks=="" || se_outof==""||te_marks==""||te_outof==""||total_marks==""||total_outof==""){
            alert("Enter all marks");
            return;
        }
        else if (average==""){        
            alert("Enter average");
            return;
        }
            $.ajax({
                type: "POST",
                url: '/editbemarks/',
                data: signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       window.location.href = "/peditotherdetails/";
                    }
                    else
                    {
                    alert('Error');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        
    }   

function editOtherDetails() {
        console.log('signupform');
        var signupform = $('#' + 'signupform');
        var csrftoken = getCookie('csrftoken');
        var birth_date = document.getElementById("birth_date").value;
        var city = document.getElementById("city").value;
        if(birth_date==""){
            alert("Enter Birth Date");
            return;
        }
        else if(city==""){
            alert("Enter city");
            return;
        }
        
            $.ajax({
                type: "POST",
                url: '/editotherdetails/',
                data: signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       window.location.href = "/presume/";
                    }
                    else
                    {
                    alert('Error');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        
    }   

function changePassword() {
       
        var csrftoken = getCookie('csrftoken');
        var old_password = document.getElementById("old_password").value;
        var new_password = document.getElementById("new_password").value;
        
            $.ajax({
                type: "POST",
                url: '/changepassword/',
                data:{old_password:old_password,new_password:new_password,csrfmiddlewaretoken:csrftoken},
                
                success: function(message) {
                console.log(message);
                    if (message =='success') {
                       alert("Password changed Successfully");
                       window.location.href = "/logout";
                    }
                    else if (message == 'wrong')
                    
                        alert('Enter correct password');
                    
                    else
                        alert("error");
                    

                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
                    
            });
    }

function companyRegister() {
        console.log('registerform');
        var registerform = $('#' + 'register');
        var csrftoken = getCookie('csrftoken');
        var name  = document.getElementById("name").value;
        var ppt_date = document.getElementById("ppt_date").value;
        var ppt_time = document.getElementById("ppt_time").value;

        if(name.length==0)
            alert('Enter name');

        else if(ppt_date.length==0 && ppt_time.length>0)
            alert("Enter date");

        else
        {
            $.ajax({
                type: "POST",
                url: '/cregister/',
                data: registerform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                    if (message =='success') {
                         window.location.href = "/";
                        alert('Registered Successfully');
                    }

                    else
                    {
                        alert('Error occured');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        }
    }


function companyUpdate() {
        console.log('updateform');
        var updateform = $('#' + 'update');
        var csrftoken = getCookie('csrftoken');
        var name = document.getElementById("company");
        var selectedvalue = name.options[name.selectedIndex].value;
        console.log(selectedvalue);
        if(selectedvalue == "Select Company")
            alert("Select Company");
        else {
            $.ajax({
                type: "POST",
                url: '/update/',
                data:updateform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                    if (message =='success') {
                        alert('Updated Successfully');
                        window.location.href = "/";

                    }

                    else
                    {
                        alert('Error occured');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        }
    }

function applyCompany(c_id){
        var checked  = document.getElementById(c_id).checked;
        console.log(checked);
        var csrftoken = getCookie('csrftoken');
        
            $.ajax({
                type: "POST",
                url: '/applycompany/',

                data:{c_id:c_id , csrfmiddlewaretoken : csrftoken,applied:checked} ,
                success: function(message) {
                    alert(message);
                    if(!(message=="Applied Successfully"||message=="Removed Application Successfully")) {
                        console.log("message");
                       if(checked)
                        document.getElementById(c_id).checked = false;
                        else
                        document.getElementById(c_id).checked = true;
                    }
                  
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        
}

function placedStudents(c_id,lock){
console.log(lock);
        if(lock=='True'){
        alert("Already Locked");
        return;
        }
        var inputs = $('tr').find('input');
        var arr=[];

        for( i=0;i<inputs.length;i++){

        if( inputs[i].checked)
        arr.push(inputs[i].id);
        }



        var csrftoken = getCookie('csrftoken');

            $.ajax({
                type: "POST",
                url: '/placedStudents/',

                data:{c_id:c_id ,placed_arr:JSON.stringify(arr), csrfmiddlewaretoken : csrftoken} ,
                success: function(message) {
                    alert(message);

                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });

}
function lockCompany(c_id,lock){

        var csrftoken = getCookie('csrftoken');
        if(lock == 1){
        alert("Already locked");
        return;
        }
            $.ajax({
                type: "POST",
                url: '/lockCompany/',

                data:{c_id:c_id , csrfmiddlewaretoken : csrftoken} ,
                success: function(message) {
                    alert(message);
                 document.getElementById("lock").innerHTML = "Locked";

                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });

}



    function loadDetails() {

        var csrftoken = getCookie('csrftoken');
        var company = document.getElementById("name").value;

            $.ajax({
                type: "POST",
                url: '/getCompanyDetails/',
                data: {company:company,csrfmiddlewaretoken:csrftoken},
                success: function(message) {
                console.log(message);
                    str  = jQuery.parseJSON(message);
                    data = str[0]["fields"];

                    criteria = data["criteria"];
                    salary = data["salary"];
                    position = data["position"];
                    back = data["back"];
                    other_details = data["other_details"];
                    
                    document.getElementById("criteria").value = criteria;
                    document.getElementById("salary").value = salary;
                    document.getElementById("position").value = position;
                    document.getElementById("back").value = back;
                    document.getElementById("other_details").value = other_details;


                    ppt = data["ppt_date"];
                    
                    if(ppt!=null){
                    var arr = ppt.split('T');
                    ppt_date = arr[0];
                    ppt_time = arr[1];

                    var date = ppt_date.split('-');
                    var year = date[0];
                    var month = date[1];
                    var dt = date[2];
                    ppt_date = month + "/"+dt + "/" + year;
                    ppt_time = ppt_time.slice(0,5);

                    document.getElementById("ppt_date").value =ppt_date;
                    document.getElementById("ppt_time").value = ppt_time;


                    }

                    
                    reg_end = data["reg_end"];
                    console.log(reg_end);
                    if(reg_end != null){
                    arr = reg_end.split('T');
                    reg_end_date = arr[0];
                    reg_end_time = arr[1].slice(0,5);


                    date = reg_end_date.split('-');
                    year = date[0];
                    month = date[1];
                    dt = date[2];
                    reg_end_date = month + "/"+dt + "/" + year;

                    document.getElementById("reg_end_date").value = reg_end_date;
                    document.getElementById("reg_end_time").value = reg_end_time;

                    }

                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });

    }

    function isValidDate(date) {
        var valid = true;
        var arr = date.split("/");
        var month = parseInt(arr[0]);
        var day   = parseInt(arr[1]);
        var year  = parseInt(arr[2]);
        console.log(month +" " +  day  +" "+ year);
        if(isNaN(month) || isNaN(day) || isNaN(year)) return false;

        if((month < 1) || (month > 12)) valid = false;
        else if((day < 1) || (day > 31)) valid = false;
        else if(((month == 4) || (month == 6) || (month == 9) || (month == 11)) && (day > 30)) valid = false;
        else if((month == 2) && (((year % 400) == 0) || ((year % 4) == 0)) && ((year % 100) != 0) && (day > 29)) valid = false;
        else if((month == 2) && ((year % 100) == 0) && (day > 29)) valid = false;
        else if((month == 2) && (day > 28)) valid = false;
        console.log(valid);
    return valid;
}

    function isValidTime(time) {
        var valid = true;
        var arr = time.split(":");
        var hr = arr[0];
        var min = arr[1];
        if(isNaN(hr) || isNaN(min)) return false;

        if((hr < 0) || (hr >= 24)) valid = false;
        else if((min < 0) || (min > 60)) valid = false;

        console.log(valid);
    return valid;
}


    function companyEdit() {
        console.log('editform');
        var registerform = $('#' + 'edit');
        var csrftoken = getCookie('csrftoken');
        var c_id = document.getElementById("name").value; //actually c_id is value
        var ppt_date = document.getElementById("ppt_date").value;
        var reg_end_date = document.getElementById("reg_end_date").value;
        var ppt_time  = document.getElementById("ppt_time").value;
        var reg_end_time = document.getElementById("reg_end_time").value;

        if(name == "Select Company")
            alert('Enter name');
        else if(ppt_date && ! isValidDate(ppt_date))
        alert("Invalid Ppt Date");
        else if(reg_end_date &&! isValidDate(reg_end_date))
        alert("Invalid Reg end date");

        else if(ppt_time && !isValidTime(ppt_time))
        alert("Invalid Ppt time");
        else if(reg_end_time && !isValidTime(reg_end_time))
        alert("Invalid Reg end time");

        else
        {
            $.ajax({
                type: "POST",
                url: '/editCompany/',
                data: registerform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
                success: function(message) {
                    if (message =='success') {
                        alert('Edited Successfully');
                         window.location.href = "/";

                    }

                    else
                    {
                        alert('Error occured');
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error');
                },
            });
        }
    }

function downloadStudents() {

        var csrftoken = getCookie('csrftoken');
        var year = document.getElementById("year").value;
        var branch = document.getElementById("branch").value;
        var minavg = document.getElementById("minavg").value;
        var maxavg = document.getElementById("maxavg").value;
        var json =  { year :year , branch :branch , minavg:minavg,maxavg:maxavg,csrfmiddlewaretoken:csrftoken};
        console.log(json);
       
        $.ajax({
            type: "POST",
            url: '/downloadstudents/',
            data:  json ,
            success: function(message) {
                console.log("success");
                var hiddenElement = document.createElement('a');
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(message);
                hiddenElement.target = '_blank';
                hiddenElement.download = year + '_' + branch + '_' + minavg + 'to' + maxavg  + '.csv';
                hiddenElement.click();
                },
            error: function(xhr, errmsg, err) {
                alert('Error'+errmsg + xhr);
            },
        });

 }

function downloadCompanies() {

        var csrftoken = getCookie('csrftoken');
        var minsal = document.getElementById("minsal").value;
        var maxsal = document.getElementById("maxsal").value;
        var mincri = document.getElementById("mincri").value;
        var maxcri = document.getElementById("maxcri").value;
        
        var json =  { mincri:mincri,maxcri:maxcri,minsal:minsal,maxsal:maxsal,csrfmiddlewaretoken:csrftoken}; 
        console.log(json);
    
        $.ajax({
            type: "POST",
            url: '/downloadcompanies/',
            data:  json ,
            success: function(message) {
                console.log("success");
                var hiddenElement = document.createElement('a');
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(message);
                hiddenElement.target = '_blank';
                hiddenElement.download = minsal  + 'to' + maxsal + 'lpa_' + mincri + 'to' + maxcri +  'per'+ '.csv';
                hiddenElement.click();
                },
            error: function(xhr, errmsg, err) {
                alert('Error');
            },
        });

 }


 function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
//function notifyCandidate() {
//        console.log('notifyform');
//        var notifyform = $('# b' + 'notify');
//        var csrftoken = getCookie('csrftoken');
//
//        $.ajax({
//            type: "POST",
//            url: '/notify/',
//            data:notifyform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
//            success: function(message) {
//                if (message =='success') {
//                    alert('Notification Sent');
//                    window.location.href = "/";
//
//                }else{
//                    alert('Error occured');
//                }
//            },
//            error: function(xhr, errmsg, err) {
//                alert('Error');
//            },
//        });
//    }

//function uploadResult() {
//        console.log('resultform');
//        var resultform = $('#' + 'result');
//        var csrftoken = getCookie('csrftoken');
//        var file = $('#resultfile')[0].files[0];
//        var data = resultform.serialize() + '&csrfmiddlewaretoken=' + csrftoken;
//        data.append('resultfile', file);
//        $.ajax({
//            type: "POST",
//            url: '/result/',
//            data:data,
//            success: function(message) {
//                if (message =='success') {
//                    alert('Result Uploaded');
//                    window.location.href = "/";
//                    }
//                else if(message == 'file'){
//                    alert("File Upload Error");
//                }else{
//                    alert('Error occured');
//                }
//            },
//            error: function(xhr, errmsg, err) {
//                alert('Error');
//            },
//        });
//    }


//function checkyear(event){
//
//    var year = this.options[this.selectedIndex].text;
//    ddl = document.getElementById("year");
//    ddl.value=year;
////     $('#year').val(year);
//
//$.ajax({
//        type: "POST",
//        url: '/year/',
//        data:  {"year":year},
//        success: function(message) {
//            document.open();
//            document.write(message);
//            document.close();
//
//             // $().html(message);
//
//        },
//        error: function(xhr, errmsg, err) {
//            alert('Error');
//        },
//    });
//
//  }
