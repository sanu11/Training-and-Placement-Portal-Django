from django.conf.urls import url
from app import views

urlpatterns = [

####Android

	url(r'verify/$',views.verify),
	url(r'register_student/$',views.register_student),
	url(r'register_company/$',views.register_company),
	url(r'update_company/$',views.update_company),
	url(r'app_login/$',views.login_details),
	url(r'app_notify/$',views.notify),
	url(r'app_sync/$',views.sync_data),

#####WEB

	url(r'^student/(?P<roll>[0-9]+)/$',views.get_student_page),
	url(r'^company/(?P<cid>[0-9]+)/$',views.get_company_page),
	url(r'^company/(?P<cid>[0-9]+)/students/$', views.get_placed_students_page),
	url(r'^hide/(?P<cid>[0-9]+)/$', views.web_hide_company),

	###admin side upload pages
	url(r'^pregister/$',views.get_register_page),
	url(r'^pupdate/$',views.get_update_page),
	url(r'^pedit/$', views.get_company_edit_page),
	url(r'^pnotify/$',views.get_notify_page),
	url(r'^presult/$',views.get_result_upload_page),	 
	url(r'^psearch/$',views.get_search_student_page),

	url(r'^cregister/$',views.web_register_company),
	url(r'^update/$',views.web_update_company),
	url(r'^editCompany/$', views.web_edit_company),
	url(r'^getCompanyDetails/$',views.get_company_details),
	url(r'^notify/$',views.web_notify),
	url(r'^result/$',views.web_upload_result),
	url(r'^changepassword/$', views.web_change_password_fromadmin),

	url(r'^roll/$',views.get_student_details),
	url(r'^lockStudent/$',views.web_lock_student),
	url(r'^unlockStudent/$',views.web_unlock_student),
    url(r'^lockAllStudents/$', views.web_lock_all_students),
    url(r'^unlockAllStudents/$', views.web_unlock_all_students),
    url(r'^updatemarksoption/$', views.web_update_marks_option),

    url(r'manage/$',views.manage),

    url(r'^(?P<c_id>[0-9]+)/viewstudents/$', views.web_view_students),
    url(r'^downloadappliedstudents/$', views.web_download_applied_students),
	url(r'^lockCompany/$', views.web_lock_company),
    url(r'^placedStudents/$', views.web_placed_students),

###student side get pages
	url(r'^psignup/$',views.get_signup_page),		
	url(r'^plogin/$',views.get_login_page),	
	url(r'^psettings/$',views.get_settings_page),



    url(r'^signup/$',views.web_signup),
	url(r'^login/$',views.web_login),
	url(r'^changepassword/$', views.web_change_password),
	url(r'^resume/$',views.web_upload_resume),
    url(r'^applycompany/$', views.web_apply_company),
    url(r'^updatemarks/$', views.web_update_marks),

	##profile pages
	url(r'^peditprofile/$',views.get_edit_profile_page),
	url(r'^peditsscmarks/$',views.get_edit_ssc_marks_page),
	url(r'^pedithscmarks/$',views.get_edit_hsc_marks_page),
	url(r'^peditbemarks/$',views.get_edit_be_marks_page),
	url(r'^peditmemarks/$', views.get_edit_me_marks_page),
	url(r'^peditotherdetails/$',views.get_edit_other_details_page),
	url(r'^presume/$',views.get_resume_upload_page),

    url(r'^editprofile/$', views.web_edit_profile),
	url(r'^editsscmarks/$', views.web_edit_ssc_marks),
	url(r'^edithscmarks/$', views.web_edit_hsc_marks),
	url(r'^editbemarks/$', views.web_edit_be_marks),
	url(r'^editmemarks/$', views.web_edit_me_marks),
	url(r'^editotherdetails/$', views.web_edit_other_details),

	url(r'^pstudentdownload/$',views.get_student_download_page),
    url(r'^pupdatemarks/$', views.get_update_marks_page),


##download pages
	url(r'^downloadstudents/$', views.web_download_students),
	url(r'^downloadcompanies/$', views.web_download_companies),
	url(r'^downloadappliedcompanies/$', views.web_download_applied_students),

##display pages
	url(r'^results/$',views.get_results_page),	 
	url(r'^companies/$',views.get_companies_page),
	url(r'^opportunities/$',views.get_opportunities_page),	 
	url(r'^appliedstudents/$',views.get_applied_students_page),	 	
	url(r'^notifications/$',views.get_notifications_page),
	url(r'^students/$',views.get_students_page),


    url(r'^logout/$',views.logout),
	url(r'^home/$',views.get_main_page),
	

	url(r'^$', views.get_main_page),
	url(r'^developers-page/$', views.get_developers_page),

]