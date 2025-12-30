from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def login_view(request):
    """
    Handles user login functionality.

    On GET: Displays the login form.
    On POST: Authenticates the provided username and password.
    If successful, logs the user in and redirects to the home page.
    If failed, shows an error message on the login page.
    """
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
    """
    Logs out the currently authenticated user and redirects to the home page.

    The @login_required decorator ensures only logged-in users can access this view.
    """
    logout(request)
    return redirect('website:home')


def signup_view(request):
    """
    Handles user registration (sign-up).

    If the user is already authenticated, redirects them to the home page.
    On GET: Displays an empty UserCreationForm.
    On POST: Validates the form and creates a new user if data is valid.
    On success: Shows success message and redirects to login page.
    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Account created successfully! You can now log in.")
                return redirect('accounts:login')

    else:
        return redirect('website:home')

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
