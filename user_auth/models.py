from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
  ROLE_CHOICES = (
    ('admin','Admin'),
    ('agent','Agent'),
    ('customer','Customer')
    )
  role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='customer')
  
  phone_number = PhoneNumberField(blank=True,null=True)
  
  
  def __str__(self):
    return self.username