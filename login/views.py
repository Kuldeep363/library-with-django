from django.shortcuts import render,redirect
from .form import loginForm
from django.contrib.auth import login,authenticate
# Create your views here.
def loginUser(request):
    login_error = pass_error = " "
    if request.method == 'POST':
        print('****************************')
        form = loginForm(request.POST)
        if len(form.data['password']) < 8:
            pass_error = 'Please enter correct password'
            print('@@@@@@@@@@@@@@@@@@')
        else:
            print('$$$$$$$$$$$$$$$$$$$$')
            username = form.data['username']
            password = form.data['password']
            user = authenticate(username = username, password = password)
            if user and user.is_active :
                login(request,user)
                return redirect('dashboard')
            else:
                login_error = 'Please use correct username or password'
    else:
        print('------------------------')
        form = loginForm()
    return render(request,'login/login.html',{'form':form,'login_error':login_error,'pass_error':pass_error}) 