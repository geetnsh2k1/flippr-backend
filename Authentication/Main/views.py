from logging import exception
from sre_parse import State
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.conf import settings

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, DealerSerializer, DriverSerializer

import random
from Main.models import usr, Dealer, Driver

FALSE_RESPONSE = {"Status":False, "Result": "FAILED"}
TRUE_RESPONSE = {"Status":True, "Result": "SUCCESSFUL"}

INVALID_CREDENTIALS = {"Status":False, "Result": "INVALID CREDENTIALS RECIEVED!"}

import json

@api_view(['POST'])
def signup(request):
    result = {"Status": True}
    try:
        email = request.data['email']
        users = User.objects.filter(email=email)
        if len(users) > 0:
            result['Status'] = False
            result['Result'] = 'Email'
        else:
            new_t = UserSerializer(data=request.data)
            if new_t.is_valid():
                new_t.save()
            else:
                result['Status'] = False
                result['Result'] = 'Username'
        
    except Exception as e:
        print(e)
        result['Status'] = False
    return Response(result)

@api_view(['GET'])
def logout(request):
    try:
        response = Response()
        response.delete_cookie('refresh_token')
        response.data = TRUE_RESPONSE
        return response
    except Exception as e:
        print(e)
        return Response(FALSE_RESPONSE)
    
# NEXT STEPS
# 1. Update user model to store access_token, refresh_token and expire date to check if token passed from request is validate token or not and also use it to generate new access_token 

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def refresh(request):
    
    attrs = { "refresh": request.COOKIES['refresh_token']}
    
    refresh = RefreshToken(attrs['refresh'])

    data = {'access': str(refresh.access_token)}

    if api_settings.ROTATE_REFRESH_TOKENS:
        if api_settings.BLACKLIST_AFTER_ROTATION:
            try:
                # Attempt to blacklist the given refresh token
                refresh.blacklist()
            except AttributeError:
                # If blacklist app not installed, `blacklist` method will
                # not be present
                pass

        refresh.set_jti()
        refresh.set_exp()

        data['refresh'] = str(refresh)

    return Response(data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def google(request):
    response = {"Status":True, "Result": "https://www.google.co.in/"}
    
    dealer_flg = False
    driver_flg = False
    
    try:
        dealer = Dealer.objects.get(user=request.user)
        dealer_flg = True
    except:
        pass
    
    if dealer_flg == False:
        try:
            driver = Driver.objects.get(user=request.user)
            driver_flg = True
        except:
            pass
    
    print(dealer_flg, driver_flg)
    
    if dealer_flg == False and driver_flg == False:
        response = {"Status": True, "Result": "Show both options"}
    
    elif driver_flg == False:
        response = {"Status": True, "Result": "dealer"}
    
    else:
        response = {"Status": True, "Result": "driver"}
    
    return Response(response)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_dealer(request):
    try:
        user = User.objects.get(username = request.data['username'])

        driver = Driver.objects.filter(user=user)
        dealer = Dealer.objects.filter(user=user)

        if len(driver) == 1:
            return Response({"status":False, "Result": "Driver with this identity already exists"})
        elif len(dealer) == 1:
            return Response({"status":False, "Result": "Dealer with this identity already exists"})
        
        new_d = Dealer.objects.create(user=user, mobile=request.data['mobile'], material_type=request.data['material_type'], material_weight=request.data['material_weight'], quantity=request.data['quantity'], city=request.data['city'], state=request.data['state'])
        new_d.save()
        return Response({"status":True})
    except Exception as e:
        print(e)
        return Response({"status":False})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_driver(request):
    try:
        user = User.objects.get(username = request.data['username'])

        driver = Driver.objects.filter(user=user)
        dealer = Dealer.objects.filter(user=user)

        if len(driver) == 1:
            return Response({"status":False, "Result": "Driver with this identity already exists"})
        elif len(dealer) == 1:
            return Response({"status":False, "Result": "Dealer with this identity already exists"})
        
        new_d = Driver.objects.create(user=user, age=request.data['age'], truck_no=request.data['truck_no'], mobile=request.data['mobile'], capacity=request.data['capacity'], transporter_name=request.data['transporter_name'], experience=request.data['experience'], routes=request.data['routes'])
        new_d.save()
        return Response({"status":True})
    except Exception as e:
        print(e)
        return Response({"status":False})

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_drivers_list(request):
    try:
        names = set()
        
        drivers = Driver.objects.filter(routes__icontains=request.data['from'])
        
        for driver in drivers:
            names.add(driver.user.username)
        
        drivers = Driver.objects.filter(routes__icontains=request.data['to'])
        
        for driver in drivers:
            names.add(driver.user.username)
            
        return Response({"status": True, "names": ' '.join(list(names))})
    except Exception as e:
        print(e)
        return Response({"status":False})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_driver(request):
    try:
        driver = Driver.objects.get(user=request.user)
        serializers = DriverSerializer(driver)
        return Response(serializers.data)
    except Exception as e:
        print(e)
        return Response({"status":False})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_dealer(request):
    try:
        dealer = Dealer.objects.get(user=request.user)
        serializers = DealerSerializer(dealer)
        return Response(serializers.data)
    except Exception as e:
        print(e)
        return Response({"status":False})

def decode(string):
    string = eval(string)
    string = string.decode()
    string = string.split('\\')
    string.pop()
    r = ""
    for number in string:
        r += chr(int(number))
    return r

@api_view(['POST'])
def send_otp(request):
    response = {}
    try:
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
            otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
            send_mail(user.email, user.username, otp)
            response = {"Status":True, "Result": otp}
        except:
            response = {"Status":False, "Result":"Invalid Username"}
    except Exception as e:
        print(e)
        response = {"Status":False, "Result":"Username not provided"}    
    return Response(response)

@api_view(['POST'])
def get_cred(request):
    response = {}
    try:
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
            crt = usr.objects.get(user=user) 
            response = {"Status":True, "Result":decode(crt.bazooka)}
        except:
            response = {"Status":False, "Result":"Invalid Username"}
    except Exception as e:
        print(e)
        response = {"Status":False, "Result":"Username not provided"}
    return Response(response)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_mail(reciever, name, otp):
    MY_ADDRESS = "johngk2164@gmail.com"
    PASSWORD = "john@1234"

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()

    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = '''Dear {name},    
Your otp for the logging in to the web application is : {otp}
    '''.format(name=name, otp=otp)

    msg['From']=MY_ADDRESS
    msg['To']=reciever
    msg['Subject'] = "Login Credentials for Web Application"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)

    del msg