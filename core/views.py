import json
import inspect
import os
import requests
import random
import uuid
import threading
import time

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from io import BytesIO
from PIL import Image

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


import arabic_reshaper
from bidi.algorithm import get_display

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError


from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.schemas.generators import BaseSchemaGenerator
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.renderers import OpenAPIRenderer
from drf_yasg.inspectors import SwaggerAutoSchema

from .serializers import *
from .models import *
from .pagination import *
from utils.utils import *

from ticket import settings



class user_view(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(CustomerSerializer(user_instance).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])


class role_view(viewsets.ModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def create(self, request, *args, **kwargs):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                ticket_instance = serializer.save()
                return Response(RoleSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])


class product_view(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])
        
    @action(detail=False, methods=['get'], url_path='count', url_name='count')
    def count(self, request, *args, **kwargs):
        try:
            product_count = Product.objects.count()
            return JsonResponse({'count': product_count})
        except Exception as e:
            return JsonResponse({'ERROR': str(e)}, status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                ticket_instance = serializer.save()
                return Response(ProductSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

        
class tools(viewsets.ViewSet):
    @swagger_auto_schema(
            method='post',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'national_id': openapi.Schema(type=openapi.TYPE_STRING)
                
                },
                required=['national_id']
            )
        )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def generate_verification_code(self, request):
        request_data = json.loads(request.body)
        national_id = request_data.get('national_id')
        code = generate_code()
        cache.set(f'verification_code_{national_id}', code, timeout=300)  
        
        send_sms(national_id, code)
        return HttpResponse('Successfully sent the code')


    @swagger_auto_schema(
            method='post',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'national_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'code': openapi.Schema(type=openapi.TYPE_STRING)
                
                },
                required=['national_id', 'code']
            )
        )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def verify_code(self, request):

        def generate_jwt_token(mobile_number):
            refresh = RefreshToken()
            refresh['national_id'] = mobile_number
            access_token = str(refresh.access_token)
            return access_token


        request_data = json.loads(request.body)
        input_code = request_data.get('code')
        user_id = request_data.get('national_id')
        cached_code = cache.get(f'verification_code_{user_id}')
        if cached_code and cached_code == input_code:
            access_token = generate_jwt_token(user_id)

            admin = Admins.objects.get(id=app_version)
            user_is_admin = any(user_id in element for element in admin.admin_phones)

            if user_is_admin:
                access_level = "admin"
            else:
                access_level = "user"


            return JsonResponse({'access_token': access_token,
                                 'access_level': access_level}, status=200)
        else:
            return HttpResponse('Invalid or expired code.', status=401)

                
class sell_view(viewsets.ViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer

    @action(detail=False, methods=['get'], url_path='all_sells_by_user/(?P<national_id>[^/.]+)')
    def all_sells_by_user(self, request, national_id=None):
        if not national_id:
            return Response({"error": "National ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        sells = Sell.objects.filter(product_owner=national_id)
        serializer = SellSerializer(sells, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='all_sells_by_user_detail/(?P<national_id>[^/.]+)')
    def all_sells_by_user_detail(self, request, national_id=None):
        if not national_id:
            return Response({"error": "National ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        sells = Sell.objects.filter(product_owner=national_id)
        sell_list = []
        
        for sell in sells:
            product = sell.product
            sell_data = SellSerializer(sell).data
            sell_data['product_name'] = product.product_name  
            sell_data['product_costs'] = product.product_cost  
            del sell_data['product']  
            sell_list.append(sell_data)
        
        return Response(sell_list, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='all_sells')
    def all_sells(self, request):
        sells = Sell.objects.all()
        serializer = SellSerializer(sells, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='all_sells_details')
    def all_sells_details(self, request):
        sells = Sell.objects.all()
        sell_list = []
        
        for sell in sells:
            product = sell.product
            sell_data = SellSerializer(sell).data
            sell_data['product_name'] = product.product_name 
            sell_data['product_costs'] = product.product_cost
            del sell_data['product']
            sell_list.append(sell_data)
        
        return Response(sell_list, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='buy_product/(?P<product_owner>[^/.]+)/(?P<product_id>[^/.]+)')
    def buy_product(self, request, product_owner=None, product_id=None):
        
        if not product_owner or not product_id:
            return Response({"error": "All fields (product_owner, product, sell_costs) are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        sell = Sell(product_owner=product_owner, product=product)
        sell.save()

        serializer = SellSerializer(sell)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        

