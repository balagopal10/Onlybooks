#dedicated for creating forms
from django import forms
from .models import  User
from django.forms import ValidationError

class MyLoginForm(forms.Form): #using Form
    username= forms.CharField(
        min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
        )
    password= forms.CharField(
        widget= forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
        )

#for registration or signup
class UserRegistrationForm(forms.ModelForm): #using ModelForm
    #password
    password= forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    #for confirm password
    password2= forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    #since inheritance from ModelForm, I can use the model to declare the fields
    class Meta:
        model= User
        #fields in the built in Model User
        fields= ('username','first_name','email','password')

        #overriding a inbuilt method to check the password input = confirm password
        #clean_<fieldname>
        def clean_password2(self):
            cd= self.cleaned_data
            if cd['password'] != cd['password2']:
                raise ValidationError('Password does not match!!!')
            
            return cd['password2']
