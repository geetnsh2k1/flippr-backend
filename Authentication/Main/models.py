from django.db import models
from django.contrib.auth.models import User

class usr(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bazooka = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.user.username
    
class Dealer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobile = models.CharField(max_length=20, blank=False, null=False)
    material_type = models.CharField(max_length=250, blank=False, null=False)
    material_weight = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=False, null=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    
    def __str__(self):
        return self.user.username
    
class Driver(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    age = models.CharField(max_length=100, blank=False, null=False)
    truck_no = models.CharField(max_length=100, blank=False, null=False)
    mobile = models.CharField(max_length=20, blank=False, null=False)
    capacity = models.CharField(max_length=100, blank=False, null=False)
    transporter_name = models.CharField(max_length=100, default="Self")
    experience = models.CharField(max_length=100, blank=False, null=False)
    routes = models.CharField(max_length=250, blank=False)
    
    booking = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.user.username