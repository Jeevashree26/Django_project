from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP validity check (e.g., 10 minutes)
        return timezone.now() < self.created_at + timezone.timedelta(minutes=10)
    

class Service(models.Model):
    name = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='service_images/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)
    address = models.TextField(default='Default Address')
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    