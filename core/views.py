import json
import inspect
import os
import requests
import random
import uuid
import threading
import time

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.shortcuts import get_object_or_404


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



class advance_view(viewsets.ViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='get_introduction_by_product_id/(?P<product_id>[^/.]+)')
    def get_introduction_by_product_id(self, request, product_id=None):
    
        introduction_text = Introduction.get_introduction_by_product_id(product_id)
        if introduction_text:
            return JsonResponse({'introduction_text': introduction_text}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': 'No introduction found for the given product ID.'}, status=404)
    
    @action(detail=False, methods=['get'], url_path='get_investigation_by_product_id/(?P<product_id>[^/.]+)')
    def get_investigation_by_product_id(self, request, product_id=None):
    
        investigation_text = Investigation.get_investigation_by_product_id(product_id)
        if investigation_text:
            return JsonResponse({'investigation_text': investigation_text}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': 'No investigation found for the given product ID.'}, status=404)


    @action(detail=False, methods=['get'], url_path='get_specification_by_product_id/(?P<product_id>[^/.]+)')
    def get_specification_by_product_id(self, request, product_id=None):
    
        specification_text = Specification.get_specification_by_product_id(product_id)
        if specification_text:
            return JsonResponse({'specification_text': specification_text}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': 'No specification found for the given product ID.'}, status=404)


    @action(detail=False, methods=['get'], url_path='get_comment_by_product_id/(?P<product_id>[^/.]+)')
    def get_comment_by_product_id(self, request, product_id=None):
    
        comment_text = Comment.get_comment_by_product_id(product_id)
        if comment_text:
            return JsonResponse({'comment_text': comment_text}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': 'No comment found for the given product ID.'}, status=404)


    @action(detail=False, methods=['get'], url_path='get_question_by_product_id/(?P<product_id>[^/.]+)')
    def get_question_by_product_id(self, request, product_id=None):
    
        question_text = Question.get_question_by_product_id(product_id)
        if question_text:
            return JsonResponse({'question_text': question_text}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': 'No question found for the given product ID.'}, status=404)

    @action(detail=False, methods=['get'], url_path='search_products/(?P<search_term>[^/.]+)')
    def search_products(self, request, search_term=None):
        if search_term:
            products = Product.search_by_name(search_term)
            product_list = [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'discount': product.discount,
                    'brand': product.brand,
                    'description': product.description,
                    'stars': product.stars,
                    'details': product.details,
                    'created_date': product.created_date
                } 
                for product in products
            ]
            return JsonResponse({'products': product_list}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': 'No search term provided.'}, status=400)


class question_view(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
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
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(QuestionSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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


class comment_view(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
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
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(CommentSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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


class introduction_view(viewsets.ModelViewSet):

    queryset = Introduction.objects.all()
    serializer_class = IntroductionSerializer
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
            serializer = IntroductionSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(IntroductionSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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



class specification_view(viewsets.ModelViewSet):

    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
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
            serializer = SpecificationSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(SpecificationSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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
			


class investigation_view(viewsets.ModelViewSet):

    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer
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
            serializer = InvestigationSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(InvestigationSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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



class category_view(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    # def list(self, request, *args, **kwargs):
    #     try:
    #         return super().list(request, *args, **kwargs)
    #     except Exception as e:
    #         err = handle_exception(get_current_class_name(), get_current_action_name())
    #         return JsonResponse({'ERROR': err[0]}, status=err[1])
    
    # def create(self, request, *args, **kwargs):
    #     try:
    #         serializer = CategorySerializer(data=request.data)
    #         if serializer.is_valid():
    #             user_instance = serializer.save()
    #             return Response(CategorySerializer(user_instance).data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         print(e)
    #         err = handle_exception(get_current_class_name(), get_current_action_name())
    #         return JsonResponse({'ERROR': err[0]}, status=err[1])

    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         return super().retrieve(request, *args, **kwargs)
    #     except Exception as e:
    #         err = handle_exception(get_current_class_name(), get_current_action_name())
    #         return JsonResponse({'ERROR': err[0]}, status=err[1])

    # def update(self, request, *args, **kwargs):
    #     try:
    #         return super().update(request, *args, **kwargs)
    #     except Exception as e:
    #         err = handle_exception(get_current_class_name(), get_current_action_name())
    #         return JsonResponse({'ERROR': err[0]}, status=err[1])

    # def partial_update(self, request, *args, **kwargs):
    #     try:
    #         return super().partial_update(request, *args, **kwargs)
    #     except Exception as e:
    #         err = handle_exception(get_current_class_name(), get_current_action_name())
    #         return JsonResponse({'ERROR': err[0]}, status=err[1])

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         return super().destroy(request, *args, **kwargs)
    #     except Exception as e:
    #         err = handle_exception(get_current_class_name(), get_current_action_name())
    #         return JsonResponse({'ERROR': err[0]}, status=err[1])
    def list(self, request):
        top_level_categories = Category.objects.filter(parent__isnull=True)
        serializer = CategorySerializer(top_level_categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='(?P<parent_category>[^/.]+)')
    def list_children(self, request, parent_category=None):
        parent = get_object_or_404(Category, name=parent_category)
        children = Category.objects.filter(parent=parent)
        serializer = CategorySerializer(children, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='(?P<parent_category>[^/.]+)/(?P<child_category>[^/.]+)')
    def list_subchildren(self, request, parent_category=None, child_category=None):
        parent = get_object_or_404(Category, name=parent_category)
        child = get_object_or_404(Category, name=child_category, parent=parent)
        subchildren = Category.objects.filter(parent=child)
        serializer = CategorySerializer(subchildren, many=True)
        return Response(serializer.data)



class group_view(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
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
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(GroupSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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



class user_view(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
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
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(UserSerializer(user_instance).data, status=status.HTTP_201_CREATED)
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


class customer_view(viewsets.ModelViewSet):

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
        categories = kwargs.get('categories', None)
        if categories:
            category_names = categories.split('/')
            parent_category = get_object_or_404(Category, name=category_names[-1])
            descendant_categories = parent_category.get_descendants(include_self=True)
            products = Product.objects.filter(category__in=descendant_categories)
        else:
            products = Product.objects.all()
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    
    
    def create(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False, methods=['get'], url_path='(?P<categories>.+)')
    # def by_category(self, request, categories=None):
    #     if categories:
    #         category_names = categories.split('/')
    #         parent_category = get_object_or_404(Category, name=category_names[-1])
    #         descendant_categories = parent_category.get_descendants(include_self=True)
    #         products = Product.objects.filter(category__in=descendant_categories)
    #     else:
    #         products = Product.objects.all()

    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)
    @action(detail=False, methods=['get'], url_path='(?P<categories>.+)')
    def retrieve_or_list_by_category(self, request, categories=None):
        if categories:
            parts = categories.split('/')

            # Check if the last part is an integer (product ID)
            try:
                product_id = int(parts[-1])
                # Retrieve product by ID
                product = get_object_or_404(Product, pk=product_id)

                # Check if we should validate the category path
                if len(parts) > 1:
                    # Extract category path excluding the product ID
                    category_names = parts[:-1]
                    for name in category_names:
                        # Check if each part of the path is a valid category
                        parent_category = get_object_or_404(Category, name=name)
                        if not (product.category in parent_category.get_descendants(include_self=True)):
                            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except ValueError:
                # If the last part is not an integer, treat it as a category path
                parent_category = get_object_or_404(Category, name=parts[-1])
                descendant_categories = parent_category.get_descendants(include_self=True)
                products = Product.objects.filter(category__in=descendant_categories)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
        
        return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        
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
        
        

