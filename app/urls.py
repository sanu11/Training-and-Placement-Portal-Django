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

	url(r'psignup/$',views.get_signup_page),		
	url(r'plogin/$',views.get_login_page),
	url(r'pregister/$',views.get_register_page),
	url(r'pupdate/$',views.get_update_page),
	url(r'pnotify/$',views.get_notify_page),

	url(r'cregister/$',views.web_register_company),
	url(r'update/$',views.web_update_company),
	url(r'notify/$',views.web_notify),
	url(r'signup/$',views.web_signup),
	url(r'login/$',views.web_login),


	
	url(r'statistics/$',views.get_statistics_page),	
	url(r'notifications/$',views.get_notifications_page),

	url(r'logout/$',views.logout),
	url(r'home/$',views.get_main_page),

	url(r'^$', views.index),



]

