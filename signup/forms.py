from django import forms
from django.contrib.auth.models import User

class signupForm(forms.ModelForm):
    username = forms.CharField(label = 'Username', widget=forms.TextInput(attrs={'class':'form-control','name':'username','id':'username'}),required = True)
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','id':'password'}),required = True)
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control','name':'password2','id':'password2'}),required = True)
    email = forms.EmailField(label = 'Email', widget=forms.EmailInput(attrs={'class':'form-control','name':'email','id':'email'}),required = True)
    first_name = forms.CharField(label = 'First Name', widget=forms.TextInput(attrs={'class':'form-control','name':'first_name','id':'first_name'}),required = True)
    last_name = forms.CharField(label = 'Last Name', widget=forms.TextInput(attrs={'class':'form-control','name':'last_name','id':'last_name'}),required = True)

    class Meta:
        model = User
        fields = ("username",'first_name','last_name','email','password')

class password_reset_form(forms.ModelForm):
    username = forms.CharField(label = 'Username', widget=forms.TextInput(attrs={'class':'form-control','name':'username','id':'username'}),required = True)

    class Meta:
        model = User
        fields = ('username',)

class password_reseting_form(forms.ModelForm):
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','id':'password'}),required = True)
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control','name':'password2','id':'password2'}),required = True)

    class Meta:
        model = User
        fields = ('password',)