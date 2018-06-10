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

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

@csrf_exempt
def login_view(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    
    user = authenticate(username=username, password=password)
    if user is None:
        response = {"status":"Invalid username or password"}
        return JsonResponse(response, status=200)

    try:
        profile = Profile.objects.get(user=user)
    except:
        return JsonResponse({"status":"No Profile Exists"}, status=200)

    if user is not None:
        request.session['username'] = username
        if(profile.user_type == 2):
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
                    "available": each.available,
                }
                items_data.append(data)

            response = {
                "items": items_data,
                "status": "login successful",
                "id": user.pk,
                "userType": user.profile.user_type
            }
        else:
            response = {
                "status": "success",
                "id": user.pk,
                "userType": user.profile.user_type
            }
        return JsonResponse(response, status=200)
        

@csrf_exempt
def logout_view(request):
    try:
      del request.session['username']
    except:
        pass
    logout(request)
    return JsonResponse({'status':"Logout Successful"})

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
        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse({"status": "Invalid Email."}, status=200)  
        
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
    try:
        cafeteria = Cafeteria.objects.get(pk=cafeteriaId)
    except:
        return JsonResponse({"status": "Cafeteria Doesn't Exist!!!"}, status=200)  

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
        "count": len(cafes)
    }
    return JsonResponse(response, status=200, safe=False)


@csrf_exempt
def getCafe(request, cafeId):
    
    try: 
        cafe = Cafe.objects.get(pk=cafeId)
    except:
        return JsonResponse({"status": "Cafe Doesn't Exists."}, status=200, safe=False)
    response = {
        "id": cafe.pk,
        "name": cafe.name,
        "cafeteriaName": cafe.cafeteria.name,
        "block": cafe.cafeteria.address.block,
        "floor": cafe.cafeteria.address.floor,
    }
    return JsonResponse(response, status=200, safe=False)
    

@csrf_exempt
def addCafe(request):
    try:
        cafeteriaUser = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({"status": "Session Invalid"}, status=200, safe=False)
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
        try:
            cafe = Cafe.objects.get(pk=int(data["cafe"]))
        except:
            return JsonResponse({"status": "Cafe Doesn't Exist"}, status=200)
        cafeteria = Cafeteria.objects.get(pk = int(cafeteriaUserProfile.request_id))

        if(cafe.cafeteria == cafeteria):
            cafe.delete()
            return JsonResponse({"status": "Cafe Deleted Successfully"}, status=200)
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def updateCafe(request): 
    cafeteriaUser = User.objects.get(username=request.session['username'])
    try:
        cafeteriaUserProfile = Profile.objects.get(user = cafeteriaUser)
    except:
        JsonResponse({"status": "Cafeteria UserProfile User Doesn't Exist"}, status=200)  

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
            "available": each.available,
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
        "available": foodItem.available,

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
                    description=data["description"],
                    category = category,
                    cafe=cafe,
                )
        foodItem.save()
        
        ingridients = data["ingredients"]
        for each in ingridients:
            ingredient = Ingredients.objects.get(pk = int(each["id"]))
            ingridientDetail = IngridientDetail(
                quantity = each["quantity"],
                foodItem = foodItem, 
                ingredient = ingredient
                )
            ingridientDetail.save()

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
        foodItemsNotAvailable = []
        foodItemsAvailable = []
        ingredientsTemp = {}
        totalRequiredQuantity = 0
        for each in items:
            foodItem = FoodItem.objects.get(pk=int(each["id"]))
            if foodItem is not None:
                totalRequiredQuantity = int(each["quantity"]) #foodItems order quntity 
                ingredientsRequired = foodItem.ingridients.all()
                print ingredientsRequired, "indadsa "
                for ingredient in ingredientsRequired:
                    ingridientDetail = IngridientDetail.objects.get(foodItem = foodItem, ingredient = ingredient)
                    ingredientQuantity = ingridientDetail.quantity #for making foodItem , to make 
                    ingredientsTemp.setdefault(ingredient.pk,"")
                    ingredientsTemp[ingredient.pk] = ingredient.availableQuantity
            else:
                return JsonResponse({"status": "Food Item Not Available."}, status=200)  
        print ingredientsTemp
        
        canBeMade = 1
        for each in items:
            flag = 0
            foodItem = FoodItem.objects.get(pk=each["id"])
            totalRequiredQuantity = int(each["quantity"]) #foodItems order quntity 
            maximumPossibleCanBeMade = 0
            
            ingredientsRequired = foodItem.ingridients.all()
            for ingredient in ingredientsRequired:
                ingridientDetail = IngridientDetail.objects.get(foodItem = foodItem, ingredient = ingredient)
                ingredientQuantity = ingridientDetail.quantity #for making foodItem , to make 
                if(ingredientsTemp[ingredient.pk] >= ingredientQuantity):
                    maxsofar = int(ingredientsTemp[ingredient.pk]/ingredientQuantity)
                    if(flag==0):
                        maximumPossibleCanBeMade = maxsofar
                        flag = 1
                    else:
                        maximumPossibleCanBeMade = min(maximumPossibleCanBeMade, maxsofar)
                    
                    if(maximumPossibleCanBeMade >= totalRequiredQuantity):
                        maximumPossibleCanBeMade = totalRequiredQuantity
                
                if (maximumPossibleCanBeMade < totalRequiredQuantity):
                    canBeMade = 0
                
                ingredientsTemp[ingredient.pk] = ingredientsTemp[ingredient.pk] - (maximumPossibleCanBeMade*ingredientQuantity)
            
            foodItemsAvailable.append({"name":foodItem.name,"Quantity" : maximumPossibleCanBeMade})    
            foodItemsNotAvailable.append({"name":foodItem.name,"Quantity" : totalRequiredQuantity -  maximumPossibleCanBeMade})


        ######################################################################
        if(canBeMade == 0):
            return JsonResponse({"status": "Insufficient Ingredients","foodItemsAvailable": foodItemsAvailable, "foodItemsNotAvailable": foodItemsNotAvailable }, status=200)


        ######################################################################
        print ingredientsTemp
        for key in ingredientsTemp.iterkeys():
            ingredient = Ingredients.objects.get(pk = key)
            ingredient.availableQuantity = ingredientsTemp[key]
            ingredient.save()
            foodItems = FoodItem.objects.all()
            for foodItem in foodItems:
                try:
                    ingridientDetail = IngridientDetail.objects.get(foodItem = foodItem, ingredient = ingredient)
                
                    quantity = ingridientDetail.quantity
                    if(quantity <= ingredientsTemp[key]):
                        foodItem.available = True
                    else:
                        foodItem.available = False
                    foodItem.save()
                except:
                    continue
        
        for each in items:
            foodItem = FoodItem.objects.get(pk=each["id"])
            quantity = int(each["quantity"])
            price  = price + (quantity*foodItem.price)
            

        order = Order(
                        customer = customer,
                        cafe = cafe,
                        note = note,
                        price = price,
                        order_status = 1,
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
        return JsonResponse({"status": "Items Ordered Successfully", "orderId": order.pk, "orderPrice": price, "order_status": ORDER_STATUS[0][1]}, status=200)
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
    elif(userProfile.user_type == 3):
        cafeteria = Cafeteria.objects.get(pk = int(userProfile.request_id))
        cafes = Cafe.objects.filter(cafeteria = cafeteria)
        cafeteriaOrders = []
        for cafe in cafes:
            cafeData = []
            orders = Order.objects.filter(cafe = cafe)
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
                cafeData.append(data)
            cafeDataValues = {
                "CafeName" : cafe.name,
                "CafeOrders" : cafeData
            }
            cafeteriaOrders.append(cafeDataValues)
        return JsonResponse({"cafeteriaOrders": cafeteriaOrders}, status=200)  
    
    return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def addIngredient(request):
    cafeteriaUser = User.objects.get(username=request.session['username'])
    cafeteriaUserProfile = Profile.objects.get(user = cafeteriaUser)
    if(cafeteriaUserProfile.user_type == 3):
        cafeteria = Cafeteria.objects.get(pk=int(cafeteriaUserProfile.request_id))
        storeHouse = StoreHouse.objects.get(cafeteria = cafeteria)

        data = json.loads(request.body)
        ingredients = Ingredients(
                    storeHouse = storeHouse,
                    name=data["name"],
                    quantity_type = data["quantity_type"],
                    availableQuantity = data["availableQuantity"],
                    description=data["description"],
                )
        ingredients.save()

        foodItems = FoodItem.objects.all()
        for foodItem in foodItems:
            try:
                ingridientDetail = IngridientDetail.objects.get(foodItem = foodItem, ingredient = ingredient)
            
                quantity = ingridientDetail.quantity
                if(quantity <= ingredients.availableQuantity):
                    foodItem.available = True
                else:
                    foodItem.available = False
                foodItem.save()
            except:
                continue

        return JsonResponse({"status": "Ingredient Added Successfully", "ingredientsId": ingredients.pk, "ingredientsName": ingredients.name}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)  

@csrf_exempt
def getIngredients(request):
    try: 
        user = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({"status": "Invalid Session."}, status=200) 
    userProfile = Profile.objects.get(user = user)
    if(userProfile.user_type == 1 or userProfile.user_type == 3):
        ingredients = Ingredients.objects.all()
        ingredients_data = []
        for each in ingredients:
            data = {
                "id": each.pk,
                "name": each.name,
                "quantity_type": QUANTITY_TYPES[int(each.quantity_type)-1][1],
                "availableQuantity": each.availableQuantity,
                "storeHouse": each.storeHouse.name,
            }
            ingredients_data.append(data)

        response = {
            "ingredients": ingredients_data,
            "count": len(ingredients)
        }
        return JsonResponse(response, status=200, safe=False)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)

@csrf_exempt
def updateIngredients(request): 
    try: 
        user = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({"status": "Invalid Session."}, status=200) 
    userProfile = Profile.objects.get(user = user)
    if(userProfile.user_type == 1 or userProfile.user_type == 3):
        data = json.loads(request.body)
        try:
            ingredient = Ingredients.objects.get(pk=int(data["ingredient"]))
        except:
            return JsonResponse({"status": "Ingredient Doesn't Exists"}, status=200)
        
        ingredient.name = data["name"]
        ingredient.quantity_type = data["quantity_type"]
        ingredient.availableQuantity = data["availableQuantity"]
        foodItems = FoodItem.objects.all()
        for foodItem in foodItems:
            try:
                ingridientDetail = IngridientDetail.objects.get(foodItem = foodItem, ingredient = ingredient)
            
                quantity = ingridientDetail.quantity
                if(quantity <= data["availableQuantity"]):
                    foodItem.available = True
                else:
                    foodItem.available = False
                foodItem.save()
            except:
                continue
        ingredient.description = data["description"]
        ingredient.save()
        return JsonResponse({"status": "ingredient Updated Successfully",}, status=200)
    else:
        return JsonResponse({"status": "You dont have required permissions."}, status=200)
