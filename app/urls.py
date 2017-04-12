from django.conf.urls import url
from app import views

urlpatterns = [
#android

	url(r'verify/$',views.verify),	
	url(r'register_student/$',views.register_student),
	url(r'register_company/$',views.register_company),
	url(r'update_company/$',views.update_company),
	url(r'app_login/$',views.login_details),
	url(r'app_notify/$',views.notify),
	url(r'app_sync/$',views.sync_data),

##web

	url(r'student/(?P<roll>[0-9]+)/$',views.get_student_page),
	url(r'company/(?P<cid>[0-9]+)/$',views.get_company_page),


	url(r'psignup/$',views.get_signup_page),		
	url(r'plogin/$',views.get_login_page),
	url(r'pregister/$',views.get_register_page),
	url(r'pupdate/$',views.get_update_page),
	url(r'pedit/$', views.get_company_edit_page),
	url(r'pnotify/$',views.get_notify_page),
	url(r'presult/$',views.get_result_upload_page),
	url(r'presume/$',views.get_resume_upload_page),

	url(r'getCompanyDetails/$',views.get_company_details),

	url(r'cregister/$',views.web_register_company),
	url(r'update/$',views.web_update_company),
	url(r'edit/$', views.web_edit_company),
	url(r'notify/$',views.web_notify),
	url(r'signup/$',views.web_signup),
	url(r'login/$',views.web_login),
	url(r'resume/$',views.web_upload_resume),
	url(r'result/$',views.web_upload_result),
	url(r'downloadstudents/$', views.web_download_students),
	url(r'downloadcompanies/$', views.web_download_companies),


	url(r'results/$',views.get_results_page),	 
	url(r'companies/$',views.get_companies_page),	 
	url(r'notifications/$',views.get_notifications_page),
	url(r'students/$',views.get_students_page),

	url(r'logout/$',views.logout),
	url(r'home/$',views.get_main_page),
	url(r'psettings/$',views.get_settings_page),

	url(r'^$', views.get_main_page),
	url(r'^developers-page/$', views.get_developers_page),


]

