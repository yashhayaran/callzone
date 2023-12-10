from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import is_valid_path
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate

'''
Home
'''


def home_view(request):
    return render(request,
                  'main/home.html',
                  {'title': 'Home'}
                  )


'''
Login
'''


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
        return redirect('/home')
    else:
        form = LoginForm()
        return render(request,
                      'registration/login.html',
                      {
                          'title': 'Login',
                          'form': form
                      }
                      )


'''
Logout
'''


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/home')


'''
Sign-up
'''


def sign_up_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            current_user = form.save()
            login(request, current_user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})
