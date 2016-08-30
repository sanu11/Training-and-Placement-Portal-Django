from django.conf.urls import url
from app import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'register/$',views.register_student),
	url(r'login/$',views.login_details),
]
