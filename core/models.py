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
    customer_address = models.CharField(max_length=255)   
    credit_balance = models.IntegerField(default=0)   
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}:{self.phone_number}"
    
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_ancestors(self):
        if self.parent:
            return self.parent.get_ancestors() + [self.parent]
        else:
            return []

    def get_full_path_list(self):
        return [ancestor.name for ancestor in self.get_ancestors()] + [self.name]

    def get_descendants(self, include_self=False):
        descendants = []
        children = Category.objects.filter(parent=self)
        for child in children:
            descendants.extend(child.get_descendants(include_self=True))
        if include_self:
            descendants.append(self)
        return descendants

class Group(models.Model):
    group_name = models.CharField(max_length=50, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category')

    def __str__(self):
        return self.group_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    brand = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    stars = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category')
    created_date = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()
    images = models.JSONField(default=list)

    def __str__(self):
        return self.name
    
    @classmethod
    def search_by_name(cls, search_term):
        return cls.objects.filter(name__icontains=search_term)
 
    

class Admins(models.Model):
    admin_group = models.CharField(max_length=50)
    admin_phones = models.JSONField(default=list)


    
    
class Sell(models.Model):
    product_owner = models.CharField(max_length=10, validators=[validate_iranian_national_id])
    product_color = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')
    buy_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"Sell for {self.product_owner}  on {self.buy_date}"
    



class Introduction(models.Model):
    introduction_text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')

    @classmethod
    def get_introduction_by_product_id(cls, product_id):
        try:
            introduction = cls.objects.get(product_id=product_id)
            return introduction.introduction_text
        except cls.DoesNotExist:
            return None

class Investigation(models.Model):
    investigation_text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')

    @classmethod
    def get_investigation_by_product_id(cls, product_id):
        try:
            investigation = cls.objects.get(product_id=product_id)
            return investigation.investigation_text
        except cls.DoesNotExist:
            return None

class Specification (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')
    specification_keys  = models.JSONField(default=list)
    specification_values  = models.JSONField(default=list)

    @classmethod
    def get_specification_by_product_id(cls, product_id):
        try:
            specification = cls.objects.get(product_id=product_id)
            zipped_specifications = zip(specification.specification_keys, specification.specification_values)
            return [{'key': key, 'value': value} for key, value in zipped_specifications]
        except cls.DoesNotExist:
            return None


class Comment(models.Model):
    comment_text = models.CharField(max_length=500) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')

    @classmethod
    def get_comment_by_product_id(cls, product_id):
        try:
            comment = cls.objects.get(product_id=product_id)
            return comment.comment_text
        except cls.DoesNotExist:
            return None

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')

    @classmethod
    def get_question_by_product_id(cls, product_id):
        try:
            question = cls.objects.get(product_id=product_id)
            return question.question_text
        except cls.DoesNotExist:
            return None
    


    


