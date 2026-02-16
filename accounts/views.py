from braces.views import AnonymousRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy("website:home")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password!")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully.")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("website:home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class SignUpView(AnonymousRequiredMixin, FormView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password!")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Account created successfully! You can now log in."
        )
        return super().form_valid(form)
