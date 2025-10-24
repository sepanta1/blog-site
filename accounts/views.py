from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def login_view(request):
    msg = ''
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('website:home')
        else:
            msg = "Invalid credentials!"
    return render(request, 'accounts/login.html', {'msg': msg})


@login_required
def logout_view(request):
    logout(request)
    return redirect('website:home')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('accounts:login')

    else:
        return redirect('website:home')

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
