from django.db import models
# Create your models here.


class UserProfileInfo(models.Model):
    # create relationship(don't inherit from User!)

    # Add any additional attributes you want
    # These name should be similar to the names in forms.py
    username = models.CharField(max_length=30, blank=False, unique=True)
    email = models.EmailField(max_length=60, blank=False, unique=True)
    confirm_email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=30, blank=False)
    confirm_password = models.CharField(max_length=30, blank=False)
    birth_date = models.DateField(blank=False)
    First_Name = models.CharField(max_length=30, blank=False)
    Last_Name = models.CharField(max_length=30, blank=False)
    Emp_ID = models.CharField(max_length=6, blank=False, unique=True)

    def __str__(self):
        return self.username+','+self.password+','+self.Emp_ID

    @classmethod
    def get(cls, param):
        pass

class loginpage(models.Model):
    password = models.CharField(max_length=30, blank=False)
    username = models.CharField(max_length=30, blank=False)
    Emp_ID = models.CharField(max_length=6, blank=True)


class Employee(models.Model):
    NAMES = models.CharField(max_length=50, unique=True, null=False)
    EMPLOYEE_ID = models.CharField(max_length=4, unique=True, null=False)
    MANAGER_ID = models.CharField(max_length=4, null=True)
    MANAGEMENT_LEVEL = models.CharField(max_length=20, null=False)
    DESIGNATION = models.CharField(max_length=20, null=False)
    STAFF = models.CharField(max_length=7 ,null=False)
    EMPLOYEE_STATUS = models.CharField(max_length=20, null=False)
    PROCESS = models.CharField(max_length=20, null=False)
    DEPARTMENT = models.CharField(max_length=15, null=False)
    TYPE_OF_SALARY = models.CharField(max_length=30, null=False)
    SALARY = models.IntegerField(null=False)
    DATE_OF_BIRTH = models.DateField(null=False)
    LOCATION_ID = models.CharField(max_length=10, null=True)
    PHONE_NUMBER = models.IntegerField(null=False)
    HIRE_DATE = models.DateField(null=False)
    END_DATE = models.DateField(null=True)
    DEPARTMENT_ID = models.CharField(max_length=10,null=True)