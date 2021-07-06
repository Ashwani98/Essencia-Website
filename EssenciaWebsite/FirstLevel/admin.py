from django.contrib import admin
from .models import UserProfileInfo, loginpage
from import_export.admin import ImportExportModelAdmin
from .models import Employee

# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(loginpage)

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('NAMES', 'EMPLOYEE_ID', 'DESIGNATION', 'EMPLOYEE_STATUS', 'HIRE_DATE')

