from django import forms
from django.forms import ModelForm

class mailForm(ModelForm):

    class meta:
        model = ''
        fields = ''      