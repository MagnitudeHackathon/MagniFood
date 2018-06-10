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
        print(request.body)
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
            return JsonResponse(response, status=200)
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
def getCafeterias(request):    
    cafeterias = Cafeteria.objects.all()
    cafeterias_data = []
    for each in cafeterias:
        data = {
            "id": each.pk,
            "name": each.name,
            "block": each.address.block,
            "floor": each.address.floor,
        }
        cafeterias_data.append(data)

    response = {
        "cafeterias": cafeterias_data,
    }

    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
def getCafeteria(request, cafeteriaId):
    cafeteria = Cafeteria.objects.get(pk=cafeteriaId)
    response = {
        "id": cafeteria.pk,
        "name": cafeteria.name,
        "block": cafeteria.address.block,
        "floor": cafeteria.address.floor,
    }
    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
def getCafes(request):    
    cafes = Cafe.objects.all()
    cafes_data = []
    for each in cafes:
        data = {
            "id": each.pk,
            "name": each.name,
            "cafeteriaName": each.cafeteria.name,
            "block": each.cafeteria.address.block,
            "floor": each.cafeteria.address.floor,
        }
        cafes_data.append(data)

    response = {
        "cafes": cafes_data,
    }
    return JsonResponse(response, status=200, safe=False)


@csrf_exempt
def getCafe(request, cafeId):
    
    try: 
        cafe = Cafe.objects.get(pk=cafeId)
        response = {
            "id": cafe.pk,
            "name": cafe.name,
            "cafeteriaName": cafe.cafeteria.name,
            "block": cafe.cafeteria.address.block,
            "floor": cafe.cafeteria.address.floor,
        }
        return JsonResponse(response, status=200, safe=False)
    except:
        return JsonResponse({"status": "Cafe Doesn't Exists."}, status=200, safe=False)

@csrf_exempt
def addCafe(request):
    cafeteriaUser = User.objects.get(username=request.session['username'])
    cafeteriaUserProfile = Profile.objects.get(user = cafeteriaUser)
    if(cafeteriaUserProfile.user_type == 3):
        data = json.loads(request.body)
        cafeteria = Cafeteria.objects.get(pk=int(data["cafeteria"]))
        cafe = Cafe(
                    name=data["name"],
                    cafeteria=cafeteria,
                )
        cafe.save()
        return JsonResponse({"status": "Cafe Added Successfully", "cafeId": cafe.pk, "cafeName": cafe.name}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def removeCafe(request):
    try:
        cafeteriaUser = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({"status": "Invalid Session."}, status=200)  
    cafeteriaUserProfile = Profile.objects.get(user = cafeteriaUser)
    if(cafeteriaUserProfile.user_type == 3):
        data = json.loads(request.body)
        cafe = Cafe.objects.get(pk=int(data["cafe"]))
        cafeteria = Cafeteria.objects.get(pk = int(cafeteriaUserProfile.request_id))

        if(cafe.cafeteria == cafeteria):
            cafe.delete()
            return JsonResponse({"status": "Cafe Deleted Successfully"}, status=200)
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def updateCafe(request): 
    cafeteriaUser = User.objects.get(username=request.session['username'])
    cafeteriaUserProfile = Profile.objects.get(user = cafeteriaUser)
    if(cafeteriaUserProfile.user_type == 3):
        data = json.loads(request.body)
        cafe = Cafe.objects.get(pk=int(data["cafe"]))
        cafeteria = Cafeteria.objects.get(pk = int(cafeteriaUserProfile.request_id))

        if(cafe.cafeteria == cafeteria):
            cafe.name = data["name"]
            cafe.save()
            return JsonResponse(
                {
                    "status": "Cafe Updated Successfully", 
                    "id": cafe.pk,
                    "name": cafe.name,
                    "cafeteriaName": cafe.cafeteria.name,
                    "block": cafe.cafeteria.address.block,
                    "floor": cafe.cafeteria.address.floor
                }, 
                status=200)
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  


@csrf_exempt
def getCompanies(request):    
    company = Company.objects.all()
    company_data = []
    for each in company:
        data = {
            "id": each.pk,
            "name": each.name,
            "block": each.address.block,
            "floor": each.address.floor,
        }
        company_data.append(data)

    response = {
        "company": company_data,
    }
    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
def getCompany(request, companyId):
    company = Company.objects.get(pk=companyId)
    response = {
        "id": company.pk,
        "name": company.name,
        "block": company.address.block,
        "floor": company.address.floor,
    }
    return JsonResponse(response, status=200, safe=False)


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
            "availableQuantity": each.availableQuantity,
        }
        items_data.append(data)

    response = {
        "items": items_data,
    }

    return JsonResponse(response, status=200, safe=False)


@csrf_exempt
def getItem(request, itemId):
    try:
        foodItem = FoodItem.objects.get(pk=itemId)
    except:
        return JsonResponse({"status": "FoodItem Doesn't Exists"}, status=200)

    response = {
        "itemId": foodItem.pk,
        "name": foodItem.name,
        "price": foodItem.price,
        "description": foodItem.description,
        "category": foodItem.category.name,
        "cafe": foodItem.cafe.name,
        "cafeteria": foodItem.cafe.cafeteria.name,
        "availableQuantity": foodItem.availableQuantity,

    }

    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
def addItem(request):
    cafeUser = User.objects.get(username=request.session['username'])
    cafeUserProfile = Profile.objects.get(user = cafeUser)
    if(cafeUserProfile.user_type == 1):
        print("cafeUserProfile.request_id:", cafeUserProfile.request_id)
        cafe = Cafe.objects.get(pk=int(cafeUserProfile.request_id))
        data = json.loads(request.body)
        category = Category.objects.get(pk = int(data["category"]))
        foodItem = FoodItem(
                    name=data["name"],
                    price=data["price"],
                    availableQuantity = data["availableQuantity"],
                    description=data["description"],
                    category = category,
                    cafe=cafe,
                )
        foodItem.save()
        return JsonResponse({"status": "FoodItem Added Successfully", "foodItemId": foodItem.pk, "foodItemName": foodItem.name}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def removeItem(request):
    try:
        cafeUser = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({"status": "Invalid UserSession"}, status=200)
    cafeUserProfile = Profile.objects.get(user = cafeUser)
    if(cafeUserProfile.user_type == 1):
        data = json.loads(request.body)
        try:
            foodItem = FoodItem.objects.get(pk=int(data["foodItem"]))
        except:
            return JsonResponse({"status": "FoodItem Doesn't Exists"}, status=200)

        cafe = Cafe.objects.get(pk = int(cafeUserProfile.request_id))

        if(foodItem.cafe == cafe):
            foodItem.delete()
            return JsonResponse({"status": "FoodItem Deleted Successfully"}, status=200)
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  


@csrf_exempt
def updateItem(request): 
    cafeUser = User.objects.get(username=request.session['username'])
    cafeUserProfile = Profile.objects.get(user = cafeUser)
    if(cafeUserProfile.user_type == 1):
        data = json.loads(request.body)
        try:
            foodItem = FoodItem.objects.get(pk=int(data["foodItem"]))
        except:
            return JsonResponse({"status": "FoodItem Doesn't Exists"}, status=200)

        cafe = Cafe.objects.get(pk = int(cafeUserProfile.request_id))

        if(foodItem.cafe == cafe):
            foodItem.name = data["name"]
            foodItem.price = data["price"]
            foodItem.availableQuantity = data["availableQuantity"]
            foodItem.description = data["description"]
            foodItem.category = Category.objects.get(pk = int(data["category"]))
            foodItem.save()
            return JsonResponse(
                {
                "status": "FoodItem Updated Successfully",
                "itemId": foodItem.pk,
                "name": foodItem.name,
                "price": foodItem.price,
                "description": foodItem.description,
                "category": foodItem.category.name,
                "cafe": foodItem.cafe.name,
                "cafeteria": foodItem.cafe.cafeteria.name,
                "availableQuantity": foodItem.availableQuantity,
                }, status=200)
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def orderItems(request):
    customer = User.objects.get(username=request.session['username'])
    customerProfile = Profile.objects.get(user=customer)

    if(customerProfile.user_type == 2):
        data = json.loads(request.body)
        try: 
            cafe = Cafe.objects.get(pk=int(data["cafe"]))
        except:
            return JsonResponse({"status": "Cafe Doesn't Exists."}, status=200, safe=False)
        
        note = data["note"]
        items = data["items"]
        foodItems = []
        price = 0
        notAvailable = []
        for each in items:
            foodItem = FoodItem.objects.get(pk=each["id"])
            if foodItem is not None:
                quantity = int(each["quantity"])
                if (quantity > foodItem.availableQuantity):
                    notAvailable.append(foodItem)

                    # return JsonResponse({"status": foodItem.name + " quantity required is not available."}, status=200)
                price = price + quantity * foodItem.price
                foodItems.append(foodItem)

            else:
                return JsonResponse({"status": "Food Item(s) Doesn't Exists"}, status=200)
        
        if(len(notAvailable) != 0):
            NAList = ""
            for each in notAvailable:
                NAList = NAList + each.name +", "
            NAList = NAList[:-2]
            return JsonResponse({"status": NAList + " quantity required is not available."}, status=200)

        for each in items:
            foodItem = FoodItem.objects.get(pk=each["id"])
            quantity = int(each["quantity"])
            foodItem.availableQuantity = foodItem.availableQuantity - quantity
            foodItem.save()

        order = Order(
                        customer = customer,
                        cafe = cafe,
                        note = note,
                        price = price,
                    )
        order.save()

        for each in items:
            quantity = int(each["quantity"])

            foodItem = FoodItem.objects.get(pk=each["id"])
            orderDetail = OrderDetail(
                quantity = quantity,
                price = foodItem.price, 
                foodItem = foodItem, 
                order = order
                )
            orderDetail.save()
        # order.foodItems.add(*foodItems)
        return JsonResponse({"status": "Items Ordered Successfully", "orderId": order.pk, "orderPrice": price}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def getOrders(request):
    try: 
        user = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({"status": "Invalid Session."}, status=200)  

    userProfile = Profile.objects.get(user = user)
    if(userProfile.user_type == 1):
        cafe = Cafe.objects.get(pk = int(userProfile.request_id))
        orders = Order.objects.filter(cafe = cafe)

        cafeOrders = []
        for each in orders:
            items = []
            for foodItem in each.foodItems.all():
                orderDetail = OrderDetail.objects.get(order = each, foodItem = foodItem)
                items.append({"name":foodItem.name, "quantity": orderDetail.quantity, "price": orderDetail.price})

            data = {
                "customer": each.customer.first_name,
                "cafe": each.cafe.name,
                "order_status": ORDER_STATUS[int(each.order_status)][1],
                "price": each.price,
                "note": each.note,
                "foodItems": items,
            }
            cafeOrders.append(data)
        print("cafeOrders", cafeOrders)
        return JsonResponse({"cafeOrders": cafeOrders}, status=200)  
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  
