import requests
import random
import os
import inspect

from django.http import FileResponse, Http404

from ticket import settings
from core.models import *
from core.melipayamak import Api


app_version = 1


def generate_code():
    return str(random.randint(10000, 99999))


def send_sms2(phone_number, verify_code):
    username = settings.SMS_PANEL_USENAME
    password = settings.SMS_PANEL_PASSWORD
    provider_phone_number = settings.SMS_PANEL_PHONE_NUMBER
    api = Api(username,password)
    sms = api.sms()
    to = phone_number
    _from = provider_phone_number
    text = verify_code
    response = sms.send(to,_from,text)
    # print(response)


def send_sms(to, text):
    username = "09197705347"
    password = "Fool@dBasa14002021"
    url = "http://api.payamak-panel.com/post/sendsms.ashx"


    customer_obj = Customer.objects.get(national_id=to)
    phone = customer_obj.phone_number

    payload = {
        "username": username,
        "password": password,
        "to": phone,
        "from": "",  # Assuming 'from' parameter should be an empty string
        "text": text
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

    
def serve_category_logo(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        if category.category_name:
            file_path = os.path.join(settings.BASE_DIR, 'static', category.category_name)
            file_extension = ".png"
            absolute_file_address = file_path + file_extension
            if os.path.exists(absolute_file_address):
                return FileResponse(open(absolute_file_address, 'rb'), content_type='image/png')
        raise Http404("Logo not found.")
    except Category.DoesNotExist:
        raise Http404("category not found.")
    
def serve_product_logo(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product_suffix = "p" + str(product_id)
        if product.name:
            file_path = os.path.join(settings.BASE_DIR, 'static', product_suffix)
            file_extension = ".png"
            absolute_file_address = file_path + file_extension
            if os.path.exists(absolute_file_address):
                return FileResponse(open(absolute_file_address, 'rb'), content_type='image/png')
        raise Http404("Logo not found.")
    except Product.DoesNotExist:
        raise Http404("category not found.")
    
def serve_product_image(request, product_id, image_id):
    try:
        product = Product.objects.get(pk=product_id)
        
        product_suffix = f"{product_id}-pic{image_id}.png"
        file_path = os.path.join(settings.BASE_DIR, 'static', product_suffix)
        
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='image/png')
        else:
            raise Http404("Image not found.")
    
    except Product.DoesNotExist:
        raise Http404("Product not found.")


def serve_slider(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'static', filename)
    return FileResponse(open(file_path, 'rb'), content_type='image/png')
    

def handle_exception(class_name, action_name):
    if settings.DEBUG:
        error_message = f"You have an error in action: {class_name}.{action_name}"
        result_status_code = 485
    else:
        error_message = "Internal Server Error"
        result_status_code = 500
    return error_message, result_status_code

def get_current_action_name():
    frame = inspect.currentframe().f_back
    action_name = inspect.getframeinfo(frame).function
    return action_name


def get_current_class_name():
    frame = inspect.currentframe().f_back
    class_name = frame.f_locals.get('self').__class__.__name__
    return class_name



