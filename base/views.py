from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from .forms import mailForm
from library import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    return render(request,'base/dashboard.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return render(request,'base/index.html')

# def verify(request):
#     return render(request,'base/mail_verification.html')
def index(request):
    return render(request,'base/index.html')

def sendMail(request):
    mailStatus = " "
    if request.method == 'POST':
        # form = mailForm(request.POST)
        data = request.POST.dict()
        name = str(data.get('username'))
        mobile = str(data.get('mobile'))
        email = str(data.get('mail'))
        msg = str(data.get('msg'))
        to = '363rawatboy@gmail.com'
        subject = 'Alert From Library'
        html_content ='<table style="border:1px solid black;border-collapse:collapse;text-align:center;"><tr style="border:1px solid black;"><th colspan="3" style="border:1px solid black;">User Data</th></tr><tr style="border:1px solid black;"><th style="border:1px solid black;">Name</th><th style="border:1px solid black;">Mobile Number</th><th style="border:1px solid black;">Email</th></tr><tr style="border:1px solid black;"><td style="border:1px solid black;">'+ name +'</td><td style="border:1px solid black;">'+ mobile +'</td><td style="border:1px solid black;">'+ email +'</td></tr><tr style="border:1px solid black;"><th colspan="3" style="border:1px solid black;">Message</th></tr><tr style="border:1px solid black;"><td colspan="3" style="border:1px solid black;">'+ msg + '</td></tr></table>'
        result = EmailMultiAlternatives(subject,msg,settings.EMAIL_HOST_USER,[to])
        result.attach_alternative(html_content, "text/html")
        result.send()

        if result: 
            mailStatus = "Thanks For Contact us!"
            return render(request,'base/index.html',{'mailStatus':mailStatus})
        else:
            mailStatus = "Try again!"
            return render(request,'base/index.html',{'mailStatus':mailStatus})
    else:
        return render(request,'base/index.html')