from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import ( signupForm, password_reset_form, password_reseting_form )
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, account_activation_token_for_pass
from django.core.mail import send_mail
from django.contrib.auth.models import User
from library import settings
# Create your views here.
def signup(request): 
    password_error = email_error = ' '
    if request.method == 'POST':
        form = signupForm(request.POST)
        if len(form.data['password'])<8:
            password_error = 'Password should be 8 characters long'
        elif form.data['password'] != form.data['password2']:
            password_error = 'Both password should be same as above'
        else:
            try:
                usr = User.objects.get(email = form.data['email'])
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                usr = None
            if usr == None:
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    print(current_site.domain)
                    mail_subject = 'Verify your email address for account activation'
                    message = render_to_string('signup/acc_activation.html',{
                            'user': user,
                            'domain':current_site.domain,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':account_activation_token.make_token(user)
                    })
                    to_mail = form.cleaned_data.get('email')
                    send_mail(mail_subject,message,settings.EMAIL_HOST_USER,[to_mail])
                    activate = 'Check your mail for account activation link.'
                    return render(request,'base/index.html',{'activate':activate})
            else:
                email_error = 'This email address is already in use'
            

    else:
        form = signupForm()
    return render(request,'signup/signup.html',{'form':form,'password_error':password_error,'email_error':email_error})


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        activate = 'Your Account Is Now Active.Enjoy🥳.Login to continue.'
        return render(request,'base/index.html',{'activate':activate})
    else:
        return HttpResponse('<div style="text-align:center;font-size:50px;line-height:300px">Activation Link Is Inavalid🚫</div>')



def passResetRequest(request):
    user_msg = ' '
    if request.method == 'POST':
        form = password_reset_form(request.POST)
        username = form.data['username']
        try:
            usr = User.objects.get(username = username)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            usr = None
            user_msg = 'This username is not exist.Please create an account'
        if usr !=None:
            print('$$$$$$$$$$$$$$$$')
            print('--------------------------')
            user = usr
            current_site = get_current_site(request)
            msg_subject = 'Password Reset Request'
            msg = render_to_string('signup/password_reset_mail.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token_for_pass.make_token(user)
                }
            )
            to_mail = usr.email 
            if to_mail == '' or to_mail == None:
                user_msg = 'Your email id is not registered. If you registered with social media account, then try using social media accounts'
            else:
                print(to_mail)
                print(type(to_mail))
                send_mail(msg_subject,msg,settings.EMAIL_HOST_USER,[to_mail])
                user_msg = 'Check your mail ID for password reset procedure.'
                return render(request,'signup/password_reset_request.html',{'form':form,'user_msg':user_msg})
    else:
        print('*******************')
        form  = password_reset_form()
    return render(request,'signup/password_reset_request.html',{'form':form,'user_msg':user_msg})
 
def reset_password(request,uidb64,token):
    pass_error = " "
    if request.method == 'POST':
        form = password_reseting_form(request.POST)
        pass1 = form.data['password']
        pass2 = form.data['password2']
        if len(pass1)<8:
            pass_error = 'Password Should be 8 characters long'
        elif pass1 != pass2:
            pass_error = 'Both passwords should be same'
        else:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk = uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExistError):
                user = None
            if user is not None or account_activation_token_for_pass.check_token(user, token):
                user.set_password(pass1)
                user.save()
                return redirect('/login')
            else:
                return HttpResponse('<div style="text-align:center;font-size:50px;line-height:300px">Password Reset Link Is Inavalid🚫 or Expired</div>') 
    else:
        form = password_reseting_form()
    return render(request,'signup/reset_password.html',{'form':form,'pass_error':pass_error,'uidb64':uidb64,'token':token})

    