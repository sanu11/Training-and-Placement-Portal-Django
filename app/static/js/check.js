

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
                else
                {
                    alert(message);
                }
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
