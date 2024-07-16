from rest_framework import serializers
from .models import *



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

def customer(data):
    serializer = CustomerSerializer(data=data)

    if serializer.is_valid():
        role_instance = serializer.save()
        return role_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'email', 'national_id', 
                  'first_name', 'last_name', 'birthday', 'role')
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

def role(data):
    serializer = RoleSerializer(data=data)

    if serializer.is_valid():
        role_instance = serializer.save()
        return role_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

def category(data):
    serializer = CategorySerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

def group(data):
    serializer = GroupSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

def comment(data):
    serializer = CommentSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class InvestigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
        fields = '__all__'

def investigation(data):
    serializer = InvestigationSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

def question(data):
    serializer = QuestionSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = '__all__'

def introduction(data):
    serializer = IntroductionSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'

def specification(data):
    serializer = SpecificationSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()
        return instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # exclude = ['logo_filename', 'product_stars']
        exclude = ['product_stars']
        # fields = '__all__'

def product(data):
    serializer = ProductSerializer(data=data)

    if serializer.is_valid():
        team_instance = serializer.save()
        return team_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
    
class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'

def create_sell(data):
    serializer = SellSerializer(data=data)

    if serializer.is_valid():
        scan_instance = serializer.save()
        return scan_instance
    else:
        errors = serializer.errors
        print(errors)
        return None

