from django.shortcuts import render, redirect
from . forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from . models import Profile
# Create your views here.


def register(request):
    template_name = "users/register.html"
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.instance.email = form.instance.username
            form.instance.first_name = form.instance.first_name.strip().title()
            form.instance.last_name = form.instance.last_name.strip().title()
            form.save()
            messages.success(request, "Your account has been created")
            return redirect('login')
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, template_name, context)
