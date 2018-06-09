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
    print (username, password, user)
    if user is not None:
        request.session['username'] = username
        response = {
            "status": "success",
            "id": user.pk,
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
    try:
      del request.session['username']
    except:
        pass
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
        
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        employeeId = data['employeeId']
        contactNumber = int(data['contactNumber'])
        
        
        workplace = data['workplace']
        


        user_type = int(data['userType'])

        if(user_type == 1):
            workplace = Cafe.objects.get(pk=int(data["workplace"]))
        elif(user_type == 2):
            workplace = Company.objects.get(pk=int(data["workplace"]))
        elif(user_type == 3):
            workplace = Cafeteria.objects.get(pk=int(data["workplace"]))

        user = User(username=username,
                     
                    first_name = first_name, 
                    last_name = last_name, 
                    email = email,
                    is_active=True,
                )
        user.set_password(password)
        try:
            user.save()
        except:
            user = User.objects.get(username=username)
            try:
                Profile.objects.get(user=user)
            except:
                response = {
                "id":user.pk,
                "name": user.first_name + user.last_name,
                "status":"User with no profile",
                }
            else:
                response = {
                    "status":"User exists",
                    "id":user.pk,
                    "name": user.first_name + user.last_name
                }
            return JsonResponse(response, status=400)
        else:
            profile = Profile(
                user = user,
                user_type=user_type,
                workplace = workplace,
                contactNumber=contactNumber,
                employeeId = employeeId,
            )
            profile.save()
            response = {
                "status":"succesful",
                "id":user.pk,
                "name": user.first_name + user.last_name,
            }
            user.set_password(password)
            user.save()
            return JsonResponse(response, status=200)

@csrf_exempt
def getItems(request):
    # foodJoint = User.objects.get(username=request.session['username'])
    
    foodItems = FoodItem.objects.all()
    items_data = []
    for each in foodItems:
        data = {
            "itemId": each.pk,
            "name": each.name,
            "price": each.price,
            "description": each.description,
            "category": each.category.name,
            "cafe": each.cafe.name,
            "cafeteria": each.cafe.cafeteria.name,
        }
        items_data.append(data)

    response = {
        "items": items_data,
    }

    return JsonResponse(response, status=200, safe=False)


@csrf_exempt
def getItem(request, itemId):
    foodItem = FoodItem.objects.get(pk=itemId)
    response = {
        "itemId": foodItem.pk,
        "name": foodItem.name,
        "price": foodItem.price,
        "description": foodItem.description,
        "category": foodItem.category.name,
        "cafe": foodItem.cafe.name,
        "cafeteria": foodItem.cafe.cafeteria.name,
    }

    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
def addItem(request):
    cafeUser = User.objects.get(username=request.session['username'])
    cafeUserProfile = Profile.objects.get(user = cafeUser)
    if(cafeUserProfile.user_type == 1):
        cafe = cafeUserProfile.workplace
        data = json.loads(request.body)
        foodItem = FoodItem(
                    name=data["name"],
                    price=data["price"],
                    availableQuantity = data["availableQuantity"],
                    description=data["description"],
                    category = data["category"],
                    cafe=cafe,
                )
        foodItem.save()
        return JsonResponse({"status": "FoodItem Added Successfully", "foodItemId": foodItem.pk}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)  


@csrf_exempt
def orderItems(request):

    
    customer = User.objects.get(username=request.session['username'])
    customerProfile = Profile.objects.get(user=customer)

    if(customerProfile.user_type == 2):
        data = json.loads(request.body)
        cafe = Cafe.objects.get(pk=int(data["cafe"]))
        note = data["note"]
        items = data["items"]
        foodItems = []
        price = 0
        for each in items:
            foodItem = FoodItem.objects.get(pk=each["id"])
            if foodItem is not None:
                quantity = int(each["quantity"])
                if (quantity > foodItem.availableQuantity):
                    return JsonResponse({"status": foodItem.name + "quantity required is not available."}, status=200)
                price = price + quantity * foodItem.price
                foodItems.append(foodItem)

            else:
                return JsonResponse({"status": "Food Item(s) Doesn't Exists"}, status=200)
        
        order = Order(
                        customer = customer,
                        cafe = cafe,
                        note = note,
                        price = price,
                    )
        order.save()
        order.foodItems.add(*foodItems)
        return JsonResponse({"status": "Items Ordered Successfully", "orderId": order.pk, "orderPrice": price}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)  
    
    