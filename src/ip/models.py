from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model

# Create your models here.

class RequestIP(models.Model):
    ip_address = models.CharField(max_length=50)
    block_time = models.DateTimeField(null=True, blank=True)
    bad_request_count = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return self.ip_address
