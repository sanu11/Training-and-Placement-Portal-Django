from django.conf.urls import url
from app import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'verify/$',views.update_company),	
	url(r'register_student/$',views.register_student),
	url(r'register_company/$',views.register_company),
	url(r'login/$',views.login_details),
	url(r'notify/$',views.notify),
	url(r'sync/$',views.sync_data),
	url(r'update_company/$',views.update_company),

]
