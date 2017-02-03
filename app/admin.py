from django.contrib import admin
from .models import Student,Company,Message,Verify,Result,Admin
from gcm.models import get_device_model

# Register your models here.
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Message)
admin.site.register(Verify)
admin.site.register(Result)
admin.site.register(Admin)
<<<<<<< HEAD


=======
>>>>>>> 7c81c50abaafe274c465a6ae70177e169d91ebc1

# admin.site.register(gcm_device)
