from django.contrib import admin
from .models import Student,Company,Message,Verify,Result,Admin,Year
from gcm.models import get_device_model

# Register your models here.
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Message)
admin.site.register(Verify)
admin.site.register(Result)
admin.site.register(Admin)
admin.site.register(Year)
# admin.site.register(gcm_device)
