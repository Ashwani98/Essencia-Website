from django.shortcuts import render
from .forms import UserForm, LoginForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
import os

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


# to upload a file
def L_T_MIS(request):
    excel_data = []
    F1 = pd.DataFrame()
    if request.method == 'POST':
        Allocation1 = request.FILES['Allocation']
        Paidfile1 = request.FILES['Paid_File']
        A = pd.read_excel(Allocation1)
        B = pd.read_excel(Paidfile1)
        # for check of file
        for i in range(0, len(A['AGREEMENTID'])):
            if pd.isnull(A['AGREEMENTID'][i]) == True:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'AGREEMENTID DOES NOT TAKE NULL VALUES'})
            elif pd.isnull(A['CUSTOMERNAME'][i]) == True or isinstance(A.loc[i,'CUSTOMERNAME'],str)==False:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'CUSTOMERNAME DOES NOT TAKE NULL VALUES'})
            elif pd.isnull(A['TC NAME'][i]) == True or isinstance(A.loc[i,'TC NAME'],str)==False:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'TC NAME DOES NOT TAKE NULL VALUES'})
            elif pd.isnull(A['TL'][i]) == True or isinstance(A.loc[i,'TL'],str)==False:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'TL DOES NOT TAKE NULL VALUES'})
            elif pd.isnull(A['FOS'][i]) == True or isinstance(A.loc[i,'FOS'],str)==False:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'FOS DOES NOT TAKE NULL VALUES'})
            elif pd.isnull(A['AREA'][i]) == True or isinstance(A.loc[i,'AREA'],str)==False:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'AREA DOES NOT TAKE NULL VALUES'})
            elif isinstance(A.loc[i,'BKT'],np.int64)==False or pd.isnull(A['BKT'][i]) == True:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'BKT DOES NOT TAKE STR VALUES'})
            elif isinstance(A.loc[i,'POS'],np.float64)==False or pd.isnull(A['POS'][i]) == True:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'POS DOES NOT TAKE STR VALUES'})
            elif isinstance(A.loc[i,'EMI'],np.int64)==False or pd.isnull(A['EMI'][i]) == True:
                print('error',i)
                return render(request, 'FirstLevel/upload_excel.html', {'error': 'EMI DOES NOT TAKE STR VALUES'})
            else:
                continue

        fs = FileSystemStorage(location='media/L_T/MIS')
        fs.save(Allocation1.name, Allocation1)
        fs.save(Paidfile1.name, Paidfile1)
        print(A.head())

        B1 = pd.DataFrame(B.groupby('AGREEMENTID')['PAID AMOUNT'].sum()).reset_index()

        for i in range(0, len(A['AGREEMENTID'])):
            for k in range(0, len(B['AGREEMENTID'])):
                if (A.loc[i, 'AGREEMENTID'] == B.loc[k, 'AGREEMENTID']) and (B.loc[k, 'AGAINST'] != 'FORECLOSE' and B.loc[k, 'AGAINST'] != 'SETTLEMENT'):
                    for j in range(0, len(B1['AGREEMENTID'])):
                        if A.loc[i, 'AGREEMENTID'] == B1.loc[j, 'AGREEMENTID']:
                            if (A.loc[i, 'BKT'] != 0 and A.loc[i, 'BKT'] != 12) and (A.loc[i, 'BKT'] != 1):
                                a = (int(A.loc[i, 'BKT']) + 1) * A.loc[i, 'EMI']
                                b = A.loc[i, 'EMI'] + A.loc[i, 'EMI']
                                if (B1.loc[j, 'PAID AMOUNT'] >= a) or (B1.loc[j, 'PAID AMOUNT'] >= A.loc[i, 'POS']):
                                    A.loc[i, 'STATUS'] = 'NM'
                                elif (B1.loc[j, 'PAID AMOUNT'] >= b) and (B1.loc[j, 'PAID AMOUNT'] < a) and (B1.loc[j, 'PAID AMOUNT'] < A.loc[i, 'POS']):
                                    A.loc[i, 'STATUS'] = 'RB'
                                elif (B1.loc[j, 'PAID AMOUNT'] >= A.loc[i, 'EMI']) and (B1.loc[j, 'PAID AMOUNT'] < b):
                                    A.loc[i, 'STATUS'] = 'SB'
                                elif B1.loc[j, 'PAID AMOUNT'] < A.loc[i, 'EMI']:
                                    A.loc[i, 'STATUS'] = 'PART PAID'
                            elif A.loc[i, 'BKT'] == 1:
                                b = A.loc[i, 'EMI'] + A.loc[i, 'EMI']
                                if (B1.loc[j, 'PAID AMOUNT'] >= b) or (B1.loc[j, 'PAID AMOUNT'] >= A.loc[i, 'POS']):
                                    A.loc[i, 'STATUS'] = 'NM'
                                elif (B1.loc[j, 'PAID AMOUNT'] >= A.loc[i, 'EMI']) and (B1.loc[j, 'PAID AMOUNT'] < b):
                                    A.loc[i, 'STATUS'] = 'SB'
                                elif B1.loc[j, 'PAID AMOUNT'] < A.loc[i, 'EMI']:
                                    A.loc[i, 'STATUS'] = 'PART PAID'
                            elif A.loc[i, 'BKT'] == 12:
                                c = (int(A.loc[i, 'BKT']) + 1) * A.loc[i, 'EMI']
                                d = A.loc[i, 'EMI'] + A.loc[i, 'EMI']
                                if (B1.loc[j, 'PAID AMOUNT'] >= c) or (B1.loc[j, 'PAID AMOUNT'] >= A.loc[i, 'POS']):
                                    A.loc[i, 'STATUS'] = 'NM'
                                elif (B1.loc[j, 'PAID AMOUNT'] >= d) and (B1.loc[j, 'PAID AMOUNT'] < c) and (B1.loc[j, 'PAID AMOUNT'] < A.loc[i, 'POS']):
                                    A.loc[i, 'STATUS'] = 'RB'
                                elif (B1.loc[j, 'PAID AMOUNT'] >= A.loc[i, 'EMI']) and (B1.loc[j, 'PAID AMOUNT'] < d):
                                    A.loc[i, 'STATUS'] = 'SB'
                                elif B1.loc[j, 'PAID AMOUNT'] < A.loc[i, 'EMI']:
                                    A.loc[i, 'STATUS'] = 'PART PAID'
                            elif A.loc[i, 'BKT'] == 0:
                                if B1.loc[j, 'PAID AMOUNT'] < A.loc[i, 'EMI']:
                                    A.loc[i, 'STATUS'] = 'PART PAID'
                                else:
                                    A.loc[i, 'STATUS'] = 'SB'
                elif (A.loc[i, 'AGREEMENTID'] == B.loc[k, 'AGREEMENTID']) and (B.loc[k, 'AGAINST'] == 'FORECLOSE'):
                    A.loc[i, 'STATUS'] = 'FORECLOSE'
                elif (A.loc[i, 'AGREEMENTID'] == B.loc[k, 'AGREEMENTID']) and (B.loc[k, 'AGAINST'] == 'SETTLEMENT'):
                    A.loc[i, 'STATUS'] = 'SETTLEMENT'
        A['STATUS'].fillna('FLOW', inplace=True)
        for i in range(0, len(A['AGREEMENTID'])):
            for j in range(0, len(B1['PAID AMOUNT'])):
                if A.loc[i, 'AGREEMENTID'] == B1.loc[j, 'AGREEMENTID']:
                    A.loc[i, 'TOTAL PAID'] = B1.loc[j, 'PAID AMOUNT']

        M = pd.DataFrame(A.groupby(['COMPANY', 'BKT', 'STATE'])['POS'].sum()).reset_index()

        M.rename({'POS': 'TOTAL_POS'}, axis=1, inplace=True)

        R = pd.DataFrame(A.groupby(['COMPANY', 'BKT', 'STATE'])['AGREEMENTID'].count()).reset_index()

        F = M.merge(R, how='outer')

        F.rename({'AGREEMENTID': 'TOTAL_CASES'}, axis=1, inplace=True)

        R1 = pd.DataFrame(A.groupby(['COMPANY', 'BKT', 'STATE', 'STATUS'])['AGREEMENTID'].count()).reset_index()

        P = F.copy()

        P = P.iloc[:, :3]

        P.head()

        P['FLOW'] = np.nan
        P['SB'] = np.nan
        P['RB'] = np.nan
        P['NM'] = np.nan
        P['PART PAID'] = np.nan
        P['FORECLOSE'] = np.nan
        P['SETTLEMENT'] = np.nan

        COL = P.columns

        for i in range(0, len(R1['COMPANY'])):
            for j in range(0, len(P['COMPANY'])):
                for k in range(0, len(COL)):
                    if ((R1.loc[i, ['COMPANY', 'BKT', 'STATE']] == P.loc[j, ['COMPANY', 'BKT', 'STATE']]).all()) and R1.loc[i, 'STATUS'] == COL[k]:
                        P.loc[j, COL[k]] = R1.loc[i, 'AGREEMENTID']

        F = F.merge(P, how='outer')

        F.fillna(0, inplace=True)

        F.rename({'FLOW': 'FLOW_CASES', 'SB': 'SB_CASES', 'RB': 'RB_CASES', 'FORECLOSE': 'FORECLOSE_CASES',
                  'SETTLEMENT': 'SETTLEMENT_CASES', 'NM': 'NM_CASES', 'PART PAID': 'PART_PAID_CASES'}, axis=1,
                 inplace=True)

        R2 = pd.DataFrame(A.groupby(['COMPANY', 'BKT', 'STATE', 'STATUS'])['POS'].sum()).reset_index()

        for i in range(0, len(R2['COMPANY'])):
            for j in range(0, len(P['COMPANY'])):
                for k in range(0, len(COL)):
                    if ((R2.loc[i, ['COMPANY', 'BKT', 'STATE']] == P.loc[j, ['COMPANY', 'BKT', 'STATE']]).all()) and R2.loc[i, 'STATUS'] == COL[k]:
                        P.loc[j, COL[k]] = R2.loc[i, 'POS']

        F = F.merge(P, how='outer')

        F.rename({'FLOW': 'FLOW_POS', 'SB': 'SB_POS', 'RB': 'RB_POS', 'FORECLOSE': 'FORECLOSE_POS', 'NM': 'NM_POS',
                  'SETTLEMENT': 'SETTLEMENT_POS', 'PART PAID': 'PART_PAID_POS'}, axis=1, inplace=True)

        F.fillna(0, inplace=True)

        for i in range(0, len(F['FLOW_CASES'])):
            F.loc[i, 'NM_POS'] = round(F.loc[i, 'NM_POS'], 2)
            F.loc[i, 'TOTAL_POS'] = round(F.loc[i, 'TOTAL_POS'], 2)
            F.loc[i, 'FLOW_POS'] = round(F.loc[i, 'FLOW_POS'], 2)
            F.loc[i, 'SB_POS'] = round(F.loc[i, 'SB_POS'], 2)
            F.loc[i, 'FLOW_POS%'] = round((F.loc[i, 'FLOW_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)
            F.loc[i, 'SB_POS%'] = round((F.loc[i, 'SB_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)
            F.loc[i, 'RB_POS%'] = round((F.loc[i, 'RB_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)
            F.loc[i, 'FORECLOSE_POS%'] = round((F.loc[i, 'FORECLOSE_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)
            F.loc[i, 'SETTLEMENT_POS%'] = round((F.loc[i, 'SETTLEMENT_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)
            F.loc[i, 'NM_POS%'] = round((F.loc[i, 'NM_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)
            F.loc[i, 'PART_PAID_POS%'] = round((F.loc[i, 'PART_PAID_POS'] / F.loc[i, 'TOTAL_POS']) * 100, 2)

        TP = pd.DataFrame(A.groupby(['COMPANY', 'BKT', 'STATE'])['TOTAL PAID'].sum()).reset_index()

        F = F.merge(TP, how='outer')

        for i in range(0, len(F['NM_CASES'])):
            F.loc[i, 'PERFORMANCE'] = F.loc[i, 'SB_POS%'] + F.loc[i, 'RB_POS%'] + F.loc[i, 'NM_POS%'] + F.loc[
                i, 'FORECLOSE_POS%'] + F.loc[i, 'SETTLEMENT_POS%']
            F.loc[i, 'Additional_Performance'] = F.loc[i, 'RB_POS%'] + F.loc[i, 'NM_POS%'] + F.loc[
                i, 'FORECLOSE_POS%'] + F.loc[i, 'SETTLEMENT_POS%']

        for i in range(0, len(F['FLOW_CASES'])):
            F.loc[i, 'PERFORMANCE'] = round(F.loc[i, 'PERFORMANCE'], 2)
            F.loc[i, 'Additional_Performance'] = round(F.loc[i, 'Additional_Performance'], 2)

        F.rename({'TOTAL_CASES': 'COUNT', 'PART_PAID_CASES': 'PP_CASES', 'FORECLOSE_CASES': 'FC_CASES',
                  'SETTLEMENT_CASES': 'SC_CASES',
                  'PART_PAID_POS': 'PP_POS', 'FORECLOSE_POS': 'FC_POS', 'SETTLEMENT_POS': 'SC_POS',
                  'FORECLOSE_POS%': 'FC_POS%',
                  'SETTLEMENT_POS%': 'SC_POS%', 'PART_PAID_POS%': 'PP_POS%', 'PERFORMANCE': 'POS_RES%'}, axis=1,
                 inplace=True)

        print(F)
        F.to_excel('media/L_T/MIS/Performance_L_T.xlsx',index=False)
        F.to_excel('media/L_T/Billing/Performance_L_T.xlsx', index=False)
        F1 = F.copy()

        for i in range(0, len(A['AGREEMENTID'])):
            s = 0
            for j in range(0, len(B['AGREEMENTID'])):
                if (A.loc[i, 'AGREEMENTID'] == B.loc[j, 'AGREEMENTID']) and ((A.loc[i, 'STATUS'] == 'FORECLOSE') or (A.loc[i, 'STATUS'] == 'SETTLEMENT') or (A.loc[i, 'STATUS'] == 'NM') or (A.loc[i, 'STATUS'] == 'RB') or (A.loc[i, 'STATUS'] == 'SB')) and ((B.loc[j, 'MODE'] != 'ECS') and (B.loc[j, 'MODE'] != 'ADJUSTED')):
                    s = s + B.loc[j, 'PAID AMOUNT']
            A.loc[i, 'Billing PAID AMT.'] = s
        for i in range(0, len(A['STATE'])):
            if A.loc[i, 'STATUS'] == 'SB':
                if A.loc[i, 'Billing PAID AMT.'] > A.loc[i, 'EMI']:
                    A.loc[i, 'Billing PAID AMT.'] = A.loc[i, 'EMI']
        A.to_excel('media/L_T/MIS/MASTER FILE L_T.xlsx', index=False)
        A.to_excel('media/L_T/Billing/MASTER FILE L_T.xlsx', index=False)
        A.to_excel('media/L_T/TC Performance/MASTER FILE L_T.xlsx', index=False)
        A.to_excel('media/L_T/FOS Salary/MASTER FILE L_T.xlsx', index=False)
        A.to_excel('media/L_T/TC Incentive/MASTER FILE L_T.xlsx', index=False)
    elif request.method != 'POST':
        if os.path.exists(r'/Users/mohaksehgal/Essencia/EssenciaWebsite/media/L_T/MIS/Performance_L_T.xlsx'):
            fs = FileSystemStorage(location='media/L_T/MIS')
            AA = fs.open('Performance_L_T.xlsx')
            F1 = pd.read_excel(AA)
        else:
            return render(request, 'FirstLevel/upload_excel.html')

    C = list(F1.columns)

    for j in range(0, len(F1[C[0]])):
        row_data = list()
        for col in range(0,len(C)):
            row_data.append(str(F1.loc[j,C[col]]))
        excel_data.append(row_data)

    return render(request, 'FirstLevel/upload_excel.html', {'excel': excel_data, 'columns': C})

def L_T_BILLING(request):
    excel_data1 = []
    F2 = pd.DataFrame()
    if request.method == 'POST':
        if os.path.exists(r'/Users/mohaksehgal/Essencia/EssenciaWebsite/media/L_T/Billing/MASTER FILE L_T.xlsx'):
            fs = FileSystemStorage(location='media/L_T/Billing')
            AA = fs.open('Performance_L_T.xlsx')
            AA1 = fs.open('MASTER FILE L_T.xlsx')
            AA2 = fs.open('AddPayout.xlsx')
            AA3 = fs.open('AddResolution.xlsx')
            AA4 = fs.open('Payout.xlsx')
            AA5 = fs.open('Resolution.xlsx')
            P = pd.read_excel(AA)
            A = pd.read_excel(AA1)
            PA = pd.read_excel(AA4)
            R = pd.read_excel(AA5)
            APA = pd.read_excel(AA2)
            AR = pd.read_excel(AA3)

            l1 = R.columns

            # =============================================================================
            # BKT 1
            # =============================================================================

            for i in range(0, len(A['BKT'])):
                if A.loc[i, 'BKT'] == 1:
                    for j in range(0, len(P['BKT'])):
                        if A.loc[i, 'BKT'] == P.loc[j, 'BKT']:
                            for k in range(0, len(l1)):
                                if l1[k] == A.loc[i, 'BKT']:
                                    for l in range(0, len(PA[1])):
                                        for y in range(0, len(APA[1])):
                                            if l == 0:
                                                if (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]]) and (P.loc[j, 'Additional_Performance'] < AR.loc[y, l1[k]]):
                                                    if (A.loc[i, 'STATUS'] == 'SB') or (A.loc[i, 'STATUS'] == 'RB' or A.loc[i, 'STATUS'] == 'NM'):
                                                        a = A.loc[i, 'Billing PAID AMT.'] * PA.loc[l, l1[k]] / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = a
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], a, P.loc[j, 'BKT'])
                                                    # =============================================================================
                                                    #                                         elif (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                                    #                                             a=(A.loc[i,'Billing PAID AMT.']*PA.loc[l,l1[k]]/100)+APA[1]
                                                    #                                             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                                    #                                             A.loc[i,'MOHAK']=a
                                                    #                                             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],a,P.loc[j,'BKT'])
                                                    # =============================================================================
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], 0, P.loc[j, 'BKT'])
                                            elif l > 0:
                                                if ((P.loc[j, 'POS_RES%'] > R.loc[l - 1, l1[k]]) and (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]])) and (P.loc[j, 'Additional_Performance'] < AR.loc[y, l1[k]]):
                                                    # =============================================================================
                                                    #                                          if (A.loc[i,'STATUS']=='RB') or (A.loc[i,'STATUS']=='NM'):
                                                    #                                              c=(A.loc[i,'Billing PAID AMT.']*PA.loc[l,l1[k]]/100)+APA[1]
                                                    #                                              A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                                    #                                              A.loc[i,'MOHAK']=int(c)
                                                    #                                              print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l-1,l1[k]],c,P.loc[j,'BKT'])
                                                    # =============================================================================
                                                    if (A.loc[i, 'STATUS'] == 'SB') or (A.loc[i, 'STATUS'] == 'NM') or (A.loc[i, 'STATUS'] == 'RB'):
                                                        d = A.loc[i, 'Billing PAID AMT.'] * (PA.loc[l, l1[k]]) / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = d
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], d, P.loc[j, 'BKT'])
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], 0, P.loc[j, 'BKT'])
                                            elif l == 6:
                                                if ((P.loc[j, 'POS_RES%'] > R.loc[l - 1, l1[k]]) and (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]])) and ((P.loc[j, 'Additional_Performance'] > AR.loc[y - 1, l1[k]]) and (P.loc[j, 'Additional_Performance'] <= AR.loc[y, l1[k]])):
                                                    if (A.loc[i, 'STATUS'] == 'RB') or (A.loc[i, 'STATUS'] == 'NM'):
                                                        c = A.loc[i, 'Billing PAID AMT.'] * (PA.loc[l, l1[k]] + APA.loc[y - 1, l1[k]]) / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]] + APA.loc[y - 1, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = c
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l - 1, l1[k]], APA.loc[y, l1[k]], c, P.loc[j, 'BKT'])
                                                    elif A.loc[i, 'STATUS'] == 'SB':
                                                        d = A.loc[i, 'Billing PAID AMT.'] * (PA.loc[l, l1[k]]) / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = d
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], APA.loc[y, l1[k]], d, P.loc[j, 'BKT'])
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], APA.loc[y, l1[k]], 0, P.loc[j, 'BKT'])

            # =============================================================================
            # BKT 2
            # =============================================================================

            for i in range(0, len(A['BKT'])):
                if A.loc[i, 'BKT'] == 2:
                    for j in range(0, len(P['BKT'])):
                        if A.loc[i, 'BKT'] == P.loc[j, 'BKT']:
                            for k in range(0, len(l1)):
                                if l1[k] == A.loc[i, 'BKT']:
                                    for l in range(0, len(PA[2])):
                                        for y in range(0, len(APA[1])):
                                            if l == 0:
                                                if (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]]) and (P.loc[j, 'Additional_Performance'] < AR.loc[y, l1[k]]):
                                                    if (A.loc[i, 'STATUS'] == 'SB') or (A.loc[i, 'STATUS'] == 'RB') or (A.loc[i, 'STATUS'] == 'NM'):
                                                        a = A.loc[i, 'Billing PAID AMT.'] * PA.loc[l, l1[k]] / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = a
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], a, P.loc[j, 'BKT'])
                                                    # =============================================================================
                                                    #                                         elif (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                                    #                                             a=(A.oc[i,'Billing PAID AMT.']*PA.loc[l,l1[k]]/100)+APA[2]
                                                    #                                             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                                    #                                             A.loc[i,'MOHAK']=a
                                                    #                                             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],a,P.loc[j,'BKT'])
                                                    # =============================================================================
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], 0, P.loc[j, 'BKT'])
                                            elif l > 0:
                                                if ((P.loc[j, 'POS_RES%'] > R.loc[l - 1, l1[k]]) and (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]])) and (P.loc[j, 'Additional_Performance'] < AR.loc[y, l1[k]]):
                                                    # =============================================================================
                                                    #                                         if (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                                    #                                             c=(A.loc[i,'Billing PAID AMT.']*(PA.loc[l,l1[k]])/100)+APA[2]
                                                    #                                             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                                    #                                             A.loc[i,'MOHAK']=int(c)
                                                    #                                             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l-1,l1[k]],c,P.loc[j,'BKT'])
                                                    # =============================================================================
                                                    if (A.loc[i, 'STATUS'] == 'SB') or (A.loc[i, 'STATUS'] == 'NM') or (A.loc[i, 'STATUS'] == 'RB'):
                                                        d = A.loc[i, 'Billing PAID AMT.'] * (PA.loc[l, l1[k]]) / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = d
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l - 1, l1[k]], d, P.loc[j, 'BKT'])
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], 0, P.loc[j, 'BKT'])
                                            # elif l>0:
                                            #     if ((P.loc[j,'POS_RES%']>R.loc[l-1,l1[k]]) and (P.loc[j,'POS_RES%']<=R.loc[l,l1[k]])) and \
                                            #     ((P.loc[j,'Additional_Performance']>AR.loc[y-1,l1[k]]) and (P.loc[j,'Additional_Performance']<=AR.loc[y,l1[k]])):
                                            #         if (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                            #             c=A.loc[i,'Billing PAID AMT.']*(PA.loc[l,l1[k]]+APA.loc[y-1,l1[k]])/100
                                            #             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]]+APA.loc[y-1,l1[k]])+'%'
                                            #             A.loc[i,'MOHAK']=c
                                            #             print(A.loc[i,'AGREEMENTID'],A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l-1,l1[k]],APA.loc[y,l1[k]],c,P.loc[j,'BKT'])
                                            #         elif A.loc[i,'STATUS']=='SB':
                                            #             d=A.loc[i,'Billing PAID AMT.']*(PA.loc[l,l1[k]])/100
                                            #             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                            #             A.loc[i,'MOHAK']=d
                                            #             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],APA.loc[y,l1[k]],d,P.loc[j,'BKT'])
                                            #         else:
                                            #             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                            #             A.loc[i,'MOHAK']=0
                                            #             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],APA.loc[y,l1[k]],0,P.loc[j,'BKT'])

            # =============================================================================
            # BKT 3
            # =============================================================================

            for i in range(0, len(A['BKT'])):
                if A.loc[i, 'BKT'] == 3:
                    for j in range(0, len(P['BKT'])):
                        if A.loc[i, 'BKT'] == P.loc[j, 'BKT']:
                            for k in range(0, len(l1)):
                                if l1[k] == A.loc[i, 'BKT']:
                                    for l in range(0, len(PA[3])):
                                        for y in range(0, len(APA[1])):
                                            if l == 0:
                                                if (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]]) and (P.loc[j, 'Additional_Performance'] < AR.loc[y, l1[k]]):
                                                    if (A.loc[i, 'STATUS'] == 'SB') or (A.loc[i, 'STATUS'] == 'RB') or (A.loc[i, 'STATUS'] == 'NM'):
                                                        a = A.loc[i, 'Billing PAID AMT.'] * PA.loc[l, l1[k]] / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = a
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], a, P.loc[j, 'BKT'])
                                                    # =============================================================================
                                                    #                                         elif (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                                    #                                             a=(A.oc[i,'Billing PAID AMT.']*PA.loc[l,l1[k]]/100)+APA[2]
                                                    #                                             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                                    #                                             A.loc[i,'MOHAK']=a
                                                    #                                             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],a,P.loc[j,'BKT'])
                                                    # =============================================================================
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], 0, P.loc[j, 'BKT'])
                                            elif l > 0:
                                                if ((P.loc[j, 'POS_RES%'] > R.loc[l - 1, l1[k]]) and (P.loc[j, 'POS_RES%'] <= R.loc[l, l1[k]])) and (P.loc[j, 'Additional_Performance'] < AR.loc[y, l1[k]]):
                                                    # =============================================================================
                                                    #                                         if (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                                    #                                             c=(A.loc[i,'Billing PAID AMT.']*(PA.loc[l,l1[k]])/100)+APA[2]
                                                    #                                             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                                    #                                             A.loc[i,'MOHAK']=int(c)
                                                    #                                             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l-1,l1[k]],c,P.loc[j,'BKT'])
                                                    # =============================================================================
                                                    if (A.loc[i, 'STATUS'] == 'SB') or (A.loc[i, 'STATUS'] == 'NM') or (A.loc[i, 'STATUS'] == 'RB'):
                                                        d = A.loc[i, 'Billing PAID AMT.'] * (PA.loc[l, l1[k]]) / 100
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = d
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l - 1, l1[k]], d, P.loc[j, 'BKT'])
                                                    else:
                                                        A.loc[i, 'PERCENTAGE'] = str(PA.loc[l, l1[k]]) + '%'
                                                        A.loc[i, 'MOHAK'] = 0
                                                        print(A.loc[i, 'AGREEMENTID'], A.loc[i, 'BKT'], P.loc[j, 'POS_RES%'], A.loc[i, 'Billing PAID AMT.'], PA.loc[l, l1[k]], 0, P.loc[j, 'BKT'])
                                            # elif l>0 and y>0:
                                            #     if ((P.loc[j,'POS_RES%']>R.loc[l-1,l1[k]]) and (P.loc[j,'POS_RES%']<=R.loc[l,l1[k]])) and \
                                            #     ((P.loc[j,'Additional_Performance']>AR.loc[y-1,l1[k]]) and (P.loc[j,'Additional_Performance']<=AR.loc[y,l1[k]])):
                                            #         if (A.loc[i,'STATUS']=='RB' or A.loc[i,'STATUS']=='NM'):
                                            #             c=A.loc[i,'Billing PAID AMT.']*(PA.loc[l,l1[k]]+APA.loc[y-1,l1[k]])/100
                                            #             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]]+APA.loc[y-1,l1[k]])+'%'
                                            #             A.loc[i,'MOHAK']=c
                                            #             print(A.loc[i,'AGREEMENTID'],A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l-1,l1[k]],APA.loc[y,l1[k]],c,P.loc[j,'BKT'])
                                            #         elif A.loc[i,'STATUS']=='SB':
                                            #             d=A.loc[i,'Billing PAID AMT.']*(PA.loc[l,l1[k]])/100
                                            #             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                            #             A.loc[i,'MOHAK']=d
                                            #             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],APA.loc[y,l1[k]],d,P.loc[j,'BKT'])
                                            #         else:
                                            #             A.loc[i,'PERCENTAGE']=str(PA.loc[l,l1[k]])+'%'
                                            #             A.loc[i,'MOHAK']=0
                                            #             print(A.loc[i,'AGREEMENTID'],A.loc[i,'BKT'],P.loc[j,'POS_RES%'],A.loc[i,'Billing PAID AMT.'],PA.loc[l,l1[k]],APA.loc[y,l1[k]],0,P.loc[j,'BKT'])

            # =============================================================================
            # SETTLEMENT
            # =============================================================================

            for i in range(0, len(A['BKT'])):
                if A.loc[i, 'STATUS'] == 'SETTLEMENT':
                    dd = A.loc[i, 'Billing PAID AMT.'] * 12 / 100
                    A.loc[i, 'MOHAK'] = dd
                    A.loc[i, 'PERCENTAGE'] = str(12) + '%'
                elif A.loc[i, 'STATUS'] == 'FORECLOSE':
                    dd = A.loc[i, 'Billing PAID AMT.'] * 20 / 100
                    A.loc[i, 'MOHAK'] = dd
                    A.loc[i, 'PERCENTAGE'] = str(20) + '%'
            # =============================================================================
            #     elif (A.loc[i,'BKT']==2 or A.loc[i,'BKT']==3) and A.loc[i,'STATUS']=='FORECLOSE':
            #         c=A.loc[i,'TOTAL COLLECTABLE']*16/100
            #         A.loc[i,'MOHAK']=c
            # =============================================================================

            A['MOHAK'].replace(np.nan, 0, inplace=True)

            A.rename({'MOHAK': 'PAYOUT'}, axis=1, inplace=True)


            A.to_excel('media/L_T/Billing/Final_Billing_L_T.xlsx', index=False)

            F = pd.DataFrame(A.groupby('BKT')['PAYOUT'].sum()).reset_index()
            for i in range(0,len(F['PAYOUT'])):
                F.loc[i,'PAYOUT']=round(F.loc[i,'PAYOUT'],2)
            F.to_excel('media/L_T/Billing/BKT_Billing_L_T.xlsx', index=False)
            F2 = F.copy()

            Total_Payout = round(sum(A['PAYOUT']),2)

        else:
            return HttpResponseRedirect(reverse('basic_app:L_T_MIS'))


    elif request.method != 'POST':
        if os.path.exists(r'/Users/mohaksehgal/Essencia/EssenciaWebsite/media/L_T/Billing/Final_Billing_L_T.xlsx'):
            fs = FileSystemStorage(location='media/L_T/Billing')
            AA = fs.open('BKT_Billing_L_T.xlsx')
            F2 = pd.read_excel(AA)
            Total_Payout = round(sum(F2['PAYOUT']),2)
        else:
            return render(request, 'FirstLevel/Billing.html')

    C1 = list(F2.columns)

    for j in range(0, len(F2[C1[0]])):
        row_data1 = list()
        for col in range(0, len(C1)):
            row_data1.append(str(F2.loc[j, C1[col]]))
        excel_data1.append(row_data1)

    return render(request, 'FirstLevel/Billing.html', {'Billing': excel_data1, 'columns': C1, 'Total_Payout': Total_Payout})