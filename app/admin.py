from django.contrib import admin
from .models import Student,Company,Message

# Register your models here.
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Message)
admin.site.register(Verify)

# admin.site.register(gcm_device)



