from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout

from .forms import MyLoginForm, UserRegistrationForm
# Create your views here.

def Index(request):
    return render(request,'home.html')
    #return HttpResponse("Welcome")
def user_login(request):
    if request.method == 'POST':
        #we will be getting username and passwords through
        login_form= MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data= login_form.cleaned_data
            auth_user= authenticate(
                request,
                username=cleaned_data['username'],
                password=cleaned_data['password']
                )
            if auth_user is not None:
                login(request, auth_user)
                #get user's role
                group= auth_user.groups.first()
                group_name= group.name if group else "No Group"
                request.session['group_name']= group_name
                return redirect('home_path')
            else:
                return HttpResponse('Not Authenticated')
    else:
        login_form=MyLoginForm()
    return render(request, 'useraccount/user_login.html',{'login_form': login_form})

def custom_logout(request):
    logout(request) #destroy all the session id for a particular user
    return redirect('login')

def register(request):
    if request.method == 'POST':
        #we will be getting username and password through POST
        user_req_form= UserRegistrationForm(request.POST)
        if user_req_form.is_valid():
            #create the form, but will not save it
            new_user= user_req_form.save(commit=False)
            #set the password after validation
            #checking password == confirm password
            #password value is assigned to password field
            new_user.set_password(
                #using set_password()
                user_req_form.cleaned_data['password'])
            new_user.save() #save to db
            return render(request, 'useraccount/register_done.html',{'user_req_form':user_req_form})
    else:
        user_req_form= UserRegistrationForm()
    return render(request, 'useraccount/register.html',{'user_req_form':user_req_form})