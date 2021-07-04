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


# for excel upload

class Allocation(models.Model):
    AGREEMENTID = models.CharField(max_length=50, unique=True)
    CUSTOMERNAME = models.CharField(max_length=50)
    COMPANY = models.CharField(max_length=50)
    BKT = models.IntegerField()
    LAST_MONTH = models.CharField(max_length=50)
    MOB = models.IntegerField(null=True)
    TOTAL_COLLECTABLE = models.IntegerField(null=True)
    POS = models.IntegerField()
    EMI = models.IntegerField()
    FOS = models.CharField(max_length=50)
    TL = models.CharField(max_length=30)
    TC_NAME = models.CharField(max_length=30)
    LOAN_TYPE = models.CharField(max_length=6, null=True)
    STATE = models.CharField(max_length=30)
    AREA = models.CharField(max_length=30)
    BOUNCING_REASONS = models.CharField(max_length=30, null=True)
    EMI_CYCLE = models.IntegerField(null=True)
    LOAN_AMT = models.IntegerField(null=True)
    ADDITIONAL_NUMBER = models.IntegerField(null=True)

class Paid_File(models.Model):
    DATE = models.DateField()
    PROCESS = models.CharField(max_length=50)
    AGREEMENTID = models.CharField(max_length=50)
    CUSTOMERNAME = models.CharField(max_length=50)
    MODE = models.CharField(max_length=50)
    EMI = models.IntegerField()
    PAID_AMOUNT = models.IntegerField()
    BOUNCING_AMOUNT = models.IntegerField()
    AGAINST = models.CharField(max_length=50)
    FOS = models.CharField(max_length=50)
    BKT = models.IntegerField()