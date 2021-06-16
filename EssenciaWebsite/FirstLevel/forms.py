from django import forms
from .models import UserProfileInfo, loginpage
# we always use .models or .forms to import data from models or forms respectively

class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    confirm_email = forms.EmailField()
    First_Name = forms.CharField()
    Last_Name = forms.CharField()
    Emp_ID = forms.CharField()
    class Meta():
        model = UserProfileInfo
        fields = '__all__'

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vemail = all_clean_data['confirm_email']
        password = all_clean_data['password']
        vpassword = all_clean_data['confirm_password']

        if (vpassword != password) or (email != vemail):
            raise forms.ValidationError('MAKE SURE PASSWORD or EMAIL MATCHES!!!')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    Emp_ID = forms.CharField()

    class Meta():
        model3 = loginpage
        fields3 = ('password', 'username', 'Emp_ID')

    def clean(self):
        all_clean_data = super().clean()
        Emp_ID = all_clean_data['Emp_ID']
        username = all_clean_data['username']
        password = all_clean_data['password']
        print(Emp_ID, username, password)

        # Taking out data from the pre saved database of UserProfileInfo
        username1 = UserProfileInfo.objects.order_by('username')
        for u in username1:
            username11 = u.username
            password1 = u.password
            Emp_ID1 = u.Emp_ID
            print(username11)
            print(password1)
            print(Emp_ID1)
            if (password != password1) or (username != username11) or (Emp_ID != Emp_ID1):
                continue
            else:
                return True
        raise forms.ValidationError('')