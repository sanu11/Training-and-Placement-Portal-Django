

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

function download() {
        console.log('studentform');
        var studentform = $('#' + 'student');
        var csrftoken = getCookie('csrftoken');
        var year = document.getElementById("year").value;
        var branch = document.getElementById("branch").value;
        var average = document.getElementById("average").value;
        var json = "&year=" + year + " &branch=" + branch + "&average=" + average;
        console.log(json);
        var json2 = "{ year :" + year + ", branch:"+ branch + ",average:" +average + ",csrfmiddlewaretoken : "+csrftoken + "}";
        console.log(json2);
        $.ajax({
            type: "POST",
            url: '/downloadstudents/',
            data: json2,
            success: function(message) {
                document.open();
                document.write(message);
                document.close();
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
