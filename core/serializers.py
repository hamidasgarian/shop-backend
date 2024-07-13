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
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

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

