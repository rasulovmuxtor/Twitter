from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder':'Email',
        'class':'form-control'
    }))
    username = forms.CharField(min_length=5,widget=forms.TextInput(attrs={
        'placeholder':'Username',
        'class':'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))

    class Meta:
        model=User
        fields=['email','username','password1','password2']


class SignInForm(forms.Form):
    username = forms.CharField(min_length=5,max_length=30,widget=forms.TextInput(attrs={
        'placeholder':'Username',
        'class':'form-control'
    }))
    password = forms.CharField(min_length=4,widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'form-control'
    }))
    