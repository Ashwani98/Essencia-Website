from django.shortcuts import render
from .forms import UserForm, LoginForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# front Page
def index(request):
    return render(request, 'FirstLevel/index.html')

# Client Page
def clients(request):
    return render(request, 'FirstLevel/clients.html')

def vision(request):
    return render(request, 'FirstLevel/vision_mission.html')

def principle(request):
    return render(request, 'FirstLevel/principle.html')

def strength(request):
    return render(request, 'FirstLevel/strength.html')

def whatwedo(request):
    return render(request, 'FirstLevel/whatwedo.html')

# After Login- Logout redirect page
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))

# for user register
def register(request):
    if request.method == 'POST':
        # taking all data from UserForm in user_form
        user_form = UserForm(data=request.POST)
        # checking the validity of user_form
        if user_form.is_valid():
            # saving the user form
            user = user_form.save()
            user.save()
            return HttpResponseRedirect(reverse('basic_app:after_register'))
        # if there will be an error
        else:
            user_form = UserForm()
            return render(request, 'FirstLevel/register.html', {'user_form': user_form, 'Error': 'MAKE SURE PASSWORD or EMAIL MATCHES!!!'})
            print(user_form.errors)
    # for first initialisation of registration page
    else:
        user_form = UserForm()
    return render(request, 'FirstLevel/register.html', {'user_form': user_form})

# login form / login page
def user_login(request):
    # checking of login form
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        # taking to username for the database
        username = request.POST.get('username')
        password = request.POST.get('password')
        Emp_id = request.POST.get('Emp_id')
        # Again Checking the form validity
        if login_form.is_valid():
            return render(request, 'FirstLevel/home.html', {'name': username})
        else:
            login_form = LoginForm()
            return render(request, 'FirstLevel/login.html', {'login_form': login_form,
                                                             'Error': 'MAKE SURE PASSWORD or EMAIL MATCHES!!!'})
            print('someone tried to login and failed!!!')
    else:
        login_form = LoginForm()
    return render(request, 'FirstLevel/login.html', {'login_form': login_form})

def after_register(request):
    # checking of login form
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        # taking to username for the database
        username = request.POST.get('username')
        # Again Checking the form validity
        if login_form.is_valid():
            return render(request, 'FirstLevel/home.html', {'name': username})
        else:
            login_form = LoginForm()
            return render(request, 'FirstLevel/login.html', {'login_form': login_form,
                                                             'Error': 'MAKE SURE PASSWORD or EMAIL MATCHES!!!'})
            print('someone tried to login and failed!!!')
    else:
        re= 'THANKS FOR REGISTER'
        login_form = LoginForm()
    return render(request, 'FirstLevel/login.html', {'login_form': login_form,'re':re})