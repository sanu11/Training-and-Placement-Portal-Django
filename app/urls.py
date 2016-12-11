from django.conf.urls import url
from app import views

urlpatterns = [
##web

url(r'notify1/$',views.get_notify_page),
	url(r'web_login/$',views.web_login),
	url(r'web_register/$',views.web_register_company),
	url(r'web_update/$',views.web_update_company),
	url(r'web_notify/$',views.web_notify),

	url(r'logout/$',views.logout),
	url(r'login_page/$',views.get_login_page),
	url(r'upload/$',views.get_upload_page),
	url(r'update/$',views.get_update_page),
	
	url(r'notifications/$',views.get_notifications_page),
	url(r'home/$',views.get_main_page),

	
	url(r'^$', views.index),

#android

	url(r'verify/$',views.verify),	
	url(r'register_student/$',views.register_student),
	url(r'register_company/$',views.register_company),
	url(r'login/$',views.login_details),
	url(r'notify/$',views.notify),
	url(r'sync/$',views.sync_data),
	url(r'update_company/$',views.update_company),




]

