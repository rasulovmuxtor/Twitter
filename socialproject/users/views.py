from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import SignInForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django import forms

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password = password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                form.add_error('password','Username or password incorrect!')
        return render(request, 'registration/login.html',{'form':form})
    form = SignInForm()
    return render(request, 'registration/login.html',{'form':form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = password)
            login(request,user)
            return redirect('home')
        return render(request, 'registration/signup.html', {'form':form})
    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})