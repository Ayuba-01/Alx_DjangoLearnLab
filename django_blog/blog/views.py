# blog/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ProfileForm

class CustomLoginView(LoginView):
    template_name = "blog/login.html"            
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = "blog/logout.html"

def registerview(request):
    """
    GET: show registration form
    POST: create user, auto-login (optional), redirect to profile or home
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log them in immediately after signup
            auth_login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("profile")  
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profileview(request):
    """
    View + edit the authenticated user's basic details.
    GET: show form with current values
    POST: validate + save; on success redirect to /profile with a success message
    """
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "blog/profile.html", {"form": form})
