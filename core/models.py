from django.db import models
from django.core import validators
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def validate_iranian_national_id(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('National ID must be a 10-digit number.')

    check = int(value[9])
    s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11

    if (s < 2 and check != s) or (s >= 2 and check != 11 - s):
        raise ValidationError('Invalid national ID.')

def generate_logo_filename(team_name):
    return f"{team_name.replace(' ', '_').lower()}_logo.png"

def only_digits_validator(value):
    if not value.isdigit():
        raise ValidationError('This field should contain only digits.')

class Role(models.Model):
    name = models.CharField(max_length=50)

    def str(self):
        return self.name

class User(AbstractUser):
    phone_number = models.CharField(max_length=11,validators=[MinLengthValidator(11)],unique=True)
    national_id = models.CharField(max_length=10,validators=[MinLengthValidator(10),only_digits_validator],unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)   
    birthday = models.DateField(null=True, blank=True) 
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}:{self.phone_number}"
    
class Customer(models.Model):
    phone_number = models.CharField(max_length=11,validators=[MinLengthValidator(11)],unique=True)
    national_id = models.CharField(max_length=10,validators=[MinLengthValidator(10),only_digits_validator],unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)   
    credit_balance = models.IntegerField(default=0)   
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}:{self.phone_number}"
    
    

class Product(models.Model):
    product_name = models.CharField(max_length=50, blank=False)
    product_cost = models.IntegerField()
    

    def __str__(self):
        return self.product_name
 
    

class Admins(models.Model):
    admin_group = models.CharField(max_length=50)
    admin_phones = models.JSONField(default=list)


    
    
class Sell(models.Model):
    product_owner = models.CharField(max_length=10, validators=[validate_iranian_national_id])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')
    buy_date = models.DateField(auto_now_add=True)
    sell_costs = models.IntegerField()
    

    def __str__(self):
        return f"Sell for {self.product_owner}  on {self.buy_date}"
    
    @classmethod
    def get_by_mobile(cls, mobile):
        return cls.objects.filter(mobile=mobile)
    


    


