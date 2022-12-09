from django.db import models
import datetime
from django.core.validators import MinValueValidator
# Create your models here.

class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    user = models.OneToOneField('auth.User', on_delete = models.CASCADE)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES ,null = True)
    phone = models.CharField(max_length = 10)
    address = models.TextField()
    is_owner = models.BooleanField(default = False)
    

class TurfImages(models.Model):
    image = models.ImageField(upload_to = 'turf_images/', null = True, blank = True)

class Turf(models.Model):
    owner = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    images = models.ManyToManyField('TurfImages')
    rent_per_hour = models.PositiveIntegerField()
    name = models.CharField(max_length = 150)
    address = models.TextField()
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6)
    latitude = models.DecimalField(max_digits = 9, decimal_places = 6)

class Bookings(models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete = models.CASCADE)
    date = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    time_from = models.TimeField()
    time_to = models.TimeField()
    order_id = models.CharField(unique=True, max_length=40, null=True, blank=True, default=None) 
    razorpay_order_id = models.CharField(max_length=40, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=40, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)


class notifications(models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    matter=models.CharField(max_length=100)
    file=models.FileField()

class owner(models.Model):
    ownerid=models.AutoField(primary_key=True)
    ownername=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    Place=models.CharField(max_length=100)
    cost=models.IntegerField()
    image=models.ImageField()
    contact=models.IntegerField()
    email=models.EmailField(max_length=20)
    remarks=models.CharField(max_length=10)

class Post(models.Model):
    username= models.CharField(max_length=100, unique=True,default='')
    ownername=models.CharField(max_length=100,default='')
    contact=models.CharField(max_length=100,default='')
    turfdetails= models.CharField(max_length=100, unique=True,default='')
    complaint= models.TextField()
    