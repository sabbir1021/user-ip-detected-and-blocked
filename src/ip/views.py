from ipaddress import ip_address
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login , logout as dj_logout
from django.contrib import messages
from .models import RequestIP
from datetime import datetime
now = datetime.now()

# Create your views here.

def home(request):
    return render(request, "index.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_ip = request.POST.get("ip")
        
        if not RequestIP.objects.filter(ip_address = user_ip).exists():
            req_ip = RequestIP.objects.create(ip_address = user_ip)
        else:
            req_ip = RequestIP.objects.get(ip_address = user_ip)
        
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dj_login(request, user)
            messages.success(request, 'You were successfully login')
            return redirect('ip:home')
        else:
            req_ip.bad_request_count = int(req_ip.bad_request_count+1)
            req_ip.save()
            messages.success(request, 'Your username password mistchmatch')
    return render(request, "login.html")