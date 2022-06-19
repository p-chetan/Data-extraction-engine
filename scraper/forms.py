from django import forms
from django.db import models
from .models import New,Buzz,PDF,Sche
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, AdminPasswordChangeForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from django.utils.translation import gettext,gettext_lazy as _


class EditScrap(forms.ModelForm):
    name = forms.CharField(label='Scraper Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={'class':'form-control'}))
    DXpath = forms.CharField(label='Table No', widget=forms.TextInput(attrs={'class':'form-control'}))
    BXpath = forms.CharField(label='DXpath', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='Email',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=New
        fields=('name','url','DXpath','BXpath','email') 

class Schedule(forms.ModelForm):
    MIN = forms.CharField(label='MIN (0-59)', widget=forms.TextInput(attrs={'class':'form-control'}))
    HR = forms.CharField(label='HR (0-23)', widget=forms.TextInput(attrs={'class':'form-control'}))
    DAYMONTH = forms.CharField(label='DAY (1-31)', widget=forms.TextInput(attrs={'class':'form-control'}))
    MONTH = forms.CharField(label='MONTH (1-12)', widget=forms.TextInput(attrs={'class':'form-control'}))
    DAYWEEK = forms.CharField(label='DAYW (1-7)',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Sche
        fields=('MIN','HR','DAYMONTH','MONTH','DAYWEEK') 


class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}     

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordChange(PasswordChangeForm):
    old_password= forms.CharField(label=_("Old Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplte':'current-password','autofocus':True,'class':'form-control'}))
    new_password1= forms.CharField(label=_("New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplte':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_("Confirm New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplte':'new-password','class':'form-control'}))

class PasswordResetForm(PasswordResetForm):
    email= forms.EmailField(label=("Email"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class SetPassword(SetPasswordForm):
    new_password1= forms.CharField(label=_("New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplte':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_("Confirm New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplte':'new-password','class':'form-control'}))

class InvestwithBuzz(forms.ModelForm):

    name = forms.CharField(label='Scraper Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    BXpath = forms.CharField(label='BXpath', widget=forms.TextInput(attrs={'class':'form-control'}))
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={'class':'form-control'}))
    DXpath = forms.CharField(label='DXpath', widget=forms.TextInput(attrs={'class':'form-control'}))
    col = forms.CharField(label='No of Columns', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model= Buzz
        fields=('name','BXpath','url','DXpath','col','email')

class PdfForm(forms.ModelForm):
    name = forms.CharField(label='Scraper Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={'class':'form-control'}))
    pages = forms.CharField(label='No of Pages', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model=PDF
        fields=('name','url','pages','email')
    
