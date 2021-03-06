from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from accounts.forms import *


def home(request):
    return render(request, 'base.html')


def registration_user(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def login_user(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("/")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "accounts/login.html", context)


def account_user(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            print(request.POST.get('photo'))
            print('---------------------------------------')
            form.save()
            context['success_message'] = "Atualizado"
    else:
        form = AccountUpdateForm(instance=request.user)

    context['account_form'] = form

    return render(request, "accounts/account.html", context)

def must_authenticate_user(request):
    return render(request, 'account/must_authenticate.html', {})
