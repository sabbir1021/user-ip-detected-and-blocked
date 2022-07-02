from django.urls import path
from . import views
app_name = "ip"

urlpatterns = [
    path('home', views.home , name="home"),
    path('', views.login , name='login'),
]