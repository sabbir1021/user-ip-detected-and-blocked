from ipaddress import ip_address
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login , logout as dj_logout
from django.contrib import messages
from .models import RequestIP
from datetime import timedelta
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, "index.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_ip = request.POST.get("ip")
        
        if not RequestIP.objects.filter(ip_address = user_ip).exists():
            req_ip = RequestIP.objects.create(ip_address = user_ip, block_time=timezone.now())
        else:
            req_ip = RequestIP.objects.get(ip_address = user_ip)
        
        if timezone.now() >= req_ip.block_time:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
                req_ip.bad_request_count = 0
                req_ip.save()
                messages.success(request, 'You were successfully login')
                return redirect('ip:home')
            else:
                if req_ip.bad_request_count == 2:
                    req_ip.block_time = timezone.now() + timedelta(hours=1)
                    req_ip.bad_request_count = 0
                    req_ip.save()
                    messages.success(request, 'Your IP is block for 1 hour')
                else:
                    req_ip.bad_request_count = int(req_ip.bad_request_count+1)
                    req_ip.save()
                    messages.success(request, 'Your username password mistchmatch')
        else:
            times = int((req_ip.block_time - timezone.now()).total_seconds()/60)
            messages.success(request, f'Your IP is block for 1 hour. After {times} min you can access.')
    return render(request, "login.html")