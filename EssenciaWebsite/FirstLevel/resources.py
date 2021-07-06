from import_export import resources
from .models import Employee

class EmployeeResources(resources.ModelResource):
    class meta:
        model = Employee()