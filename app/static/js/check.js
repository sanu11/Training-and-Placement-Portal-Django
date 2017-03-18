

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

function companyRegister() {
        console.log('registerform');
        var registerform = $('#' + 'register');
        var csrftoken = getCookie('csrftoken');
        console.log('registerform');
        $.ajax({
            type: "POST",
            url: '/cregister/',
            data: registerform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
            success: function(message) {
                if (message =='success') {
                    alert('Registered Successfully');
                     window.location.href = "/";

                }
                else if(message=='exists')
                {
                    alert("Already registered.")
                    location.reload();
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

function companyUpdate() {
        console.log('updateform');
        var updateform = $('#' + 'update');
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            type: "POST",
            url: '/update/',
            data:updateform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
            success: function(message) {
                if (message =='success') {
                    alert('Updated Successfully');
                    window.location.href = "/";

                }
                else if(message=='updated')
                {
                    alert("Already Updated.")
                    location.reload();
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
                alert('Error');
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
//        var notifyform = $('#' + 'notify');
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


//function signup() {
//        console.log('signup');
//        var signupform = $('#' + 'signup');
//        var csrftoken = getCookie('csrftoken');
//
//        $.ajax({
//            type: "POST",
//            url: '/signup/',
//            data:signupform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
//            success: function(message) {
//                if (message =='success') {
//                    alert('Registered Successfully');
//                    window.location.href = "/";
//
//                }else if(message == 'exists'){
//                    alert('User Exists.Please Login');
//                    window.location.href ="/plogin/";
//                }
//                else{
//                    alert('Error Occured');
//                    }
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
