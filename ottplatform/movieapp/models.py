from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone

class AdminLogin(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=128)
    forgotkey = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=50,default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class MovieList(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video = models.FileField(upload_to='videos/')
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class PlanModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default=True) 
    def __str__(self):
        return self.name
 

class Userhistory(models.Model):
    userid = models.ForeignKey(AdminLogin, on_delete=models.CASCADE, null=True)
    movieid = models.ForeignKey(MovieList, on_delete=models.CASCADE, null=True)
    Date_and_Time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.userid.name} - {self.movieid.title} - {self.Date_and_Time}"
    

class Subscriber(models.Model):
    userid = models.ForeignKey(AdminLogin, on_delete=models.CASCADE, null=True)  
    planid = models.ForeignKey(PlanModel, on_delete=models.CASCADE, null=True)
    startdate = models.DateField(default=timezone.now)
    end_date = models.DateField()
    year = models.PositiveIntegerField(blank=True, null=True)
    month = models.PositiveIntegerField(blank=True, null=True)
    payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default=True) 
    def save(self, *args, **kwargs):
        if self.startdate:
            self.year = self.startdate.year
            self.month = self.startdate.month
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.userid.name} - {self.planid.name}"
