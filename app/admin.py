from django.contrib import admin
from .models import Student,Company,Message,Verify,Result,Admin,Year
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from gcm.models import get_device_model

# Register your models here.


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
        import_id_fields = ['s_id']

class CompanyResource(resources.ModelResource):

    class Meta:
        model = Company
        import_id_fields = ['c_id']

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class =  StudentResource

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource
    readonly_fields=('c_id',)

@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    pass

@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    pass

@admin.register(Verify)
class VerifyAdmin(ImportExportModelAdmin):
    pass

@admin.register(Admin)
class Admin(ImportExportModelAdmin):
    pass

@admin.register(Year)
class YearAdmin(ImportExportModelAdmin):
    pass


# admin.site.register(gcm_device)
