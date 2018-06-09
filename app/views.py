from __future__ import unicode_literals
from django.shortcuts import render
import xlrd
from .models import *
from django.http import JsonResponse, HttpResponse
import json
# from urllib.request import urlopen
# from urllib.request import urlopen, Request

import operator
from django.core import serializers as surr

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    user = authenticate(username=username, password=password)
    print (username, password)
    if user is not None:
        response = {
            "status":"success",
            "id":user.pk,
            "userType": user.profile.user_type
        }
        return JsonResponse(response, status=200)
    else:
        response = {
            "status":"failed",
        }
        return JsonResponse(response, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'error':False})

@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        return render(request, "signup.html", {})
    elif request.method == 'POST':
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        name = data['name']
        phone = int(data['phone'])
        address = data['address']
        user_type = int(data['userType'])
        sex  = int(data['sex'])

        user = User(username=username, is_active=True)
    try:
        user.save()
    except:
        user = User.objects.get(username=username)
        try:
            Profile.objects.get(user=user)
        except:
            response = {
            "id":user.pk,
            "status":"exists_but_no_profile",
            }
        else:
            response = {
            "status":"exists",
            "id":user.pk,
            "name": profile.name,
            }
        return JsonResponse(response, status=400)
    else:
        profile = Profile(
            user=user, 
            name=name,
            contactNumber=phone,
            address=address,
            user_type=user_type,
            sex=sex,
        )
        profile.save()
        response = {
            "status":"succesfull",
            "id":user.pk,
            "name": profile.name,
        }
        user.set_password(password)
        user.save()
        return JsonResponse(response, status=200)

@csrf_exempt
def editUser_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        # print("data=", data)
        username = data['username']
        password = data['password']

        name = data['name']
        age = int(data['age'])
        phone = int(data['phone'])
        address = data['address']
        od = float(data['od'])
        os = float(data['os'])
        va = float(data['va'])

        user = authenticate(request, username=username, password=password)
        if user is not None:
            pgOwner = PgOwners.objects.get(user=user)
            profile = Profile.objects.get(user = user)
            profile.name = name
            profile.age = age
            profile.phone = phone
            profile.address = address
            profile.od = od
            profile.os = os
            profile.va = va
            profile.save()

            return JsonResponse({'msg':"User updated successfully", 'error':False})
    else:
        return JsonResponse({'msg':"Page doesn't exists.", 'error':True})


@csrf_exempt
def getProfile(request, user_id):
    user = User.objects.get(pk=user_id)
    if user:
        profile = Profile.objects.get(user=user)
        if profile.photo:
            imageUrl = profile.photo.url
        else:
            imageUrl = "None"
        
        if profile.aadharCard:
            aadharCardUrl = profile.aadharCard.url
        else:
            aadharCardUrl = "None"
        
        response = {
            "userId":user_id,
            "username":user.username,
            "profileId": profile.id,
            "name": profile.name,
            "contactNumber": profile.contactNumber,
            "address": profile.address,
            "dob": profile.dob,
            "photo": imageUrl,
            "aadharCard": aadharCardUrl,
            "sex": profile.sex,
        }
        return JsonResponse(response, status=200)
    else:
        response = {"User not found, wrong id"}
        return JsonResponse(response, status=404)

@csrf_exempt
def getProducts(request):
    products = Products.objects.all()
    products_data = []
    for each in products:
        print("each.costingType:", each.costingType)
        data = {
            "name": each.name,
            "cost": each.cost,
            "costingType": COSTING_CHOICS[int(each.costingType)][1],
            "description": each.description,
            "seller": each.seller.profile.name
        }
        products_data.append(data)

    response = {
        "products": products_data,
    }
    print(response)

    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
def addProduct(request, sellerId):
    user = User.objects.get(pk=sellerId)
    
    data = json.loads(request.body)
    room = Products(
                name=data["name"],
                cost=data["cost"],
                description=data["description"],
                seller=user
            )
    room.save()
    return JsonResponse({"message": "Room Added Successfully"}, status=200)