from django import forms
from django.forms import ModelForm
from .models import books
class addForm(ModelForm):
    price = forms.IntegerField(label='Price',widget = forms.NumberInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='Description',widget = forms.Textarea(attrs={'class': 'form-control '}))
    class Meta:
        model = books
        fields = ("price","description")

class form_add(ModelForm):
    title = forms.CharField(label='Title',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title or Name of Book',}),required=False)
    price = forms.IntegerField(label='Price',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Price'}),required=False)
    description = forms.CharField(label='Description',widget = forms.Textarea(attrs={'class': 'form-control','placeholder':'Some words for book'}),required=False)
    authors = forms.CharField(label='Authors',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Separate authors name with comma(,)'}),required=False)
    subject = forms.CharField(label='Subject',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Subject or domain of book'}),required=False)
    image = forms.ImageField(label='Cover Photo',widget=forms.FileInput(attrs={'class':'form-control'}),required=False)
    pdf_file = forms.FileField(label='PDF FILE',widget=forms.FileInput(attrs={'class':'form-control'}),required=False)

    class Meta:
        model = books
        fields = ('title','price','description','authors','subject','image','pdf_file')