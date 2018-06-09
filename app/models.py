from __future__ import unicode_literals


from django.db import models
from django.utils import timezone

# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from MagniFood import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


USER_TYPES = (
    (1, "CafeUser"),
    (2, "Customer"),
    (3, "CafeteriaUser"),
)

ORDER_STATUS = (
    (1, "Ordered"),
    (2, "Confirmed"),
    (3, "Ready"),
    (4, "Delivered")
)

WORKPLACE_TYPES = (
    (1, "Cafe"),
    (2, "Company"),
    (3, "Cafeteria"),
)

class Address(models.Model):
    block  = models.CharField(max_length=150, null=True,blank=True)
    floor = models.CharField(max_length=150, null=True,blank=True)
    def __str__(self):
        return "Block : "+self.block + " Floor : "+self.floor
    
class Cafeteria(models.Model):
    name  = models.CharField(max_length=150, null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Cafe(models.Model):
    name  = models.CharField(max_length=150, null=True,blank=True)
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Company(models.Model):
    name  = models.CharField(max_length=150, null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name


# class Workplace(models.Model):
#     workplace_type = models.IntegerField(default=2, choices=WORKPLACE_TYPES)
#     name  = models.CharField(max_length=150, null=True,blank=True)
#     block  = models.CharField(max_length=150, null=True,blank=True)
#     floor = models.CharField(max_length=150, null=True,blank=True)
#     def __str__(self):
#         return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(default=2, choices=USER_TYPES)
    date_added = models.DateTimeField(default=timezone.now)
    # workplace = models.ForeignKey(Workplace,on_delete=models.CASCADE, null=True, blank=True)
    request_type = models.ForeignKey(ContentType, null=True, blank=True)
    request_id = models.PositiveIntegerField(null=True, blank=True)
    workplace = GenericForeignKey('request_type', 'request_id')
    contactNumber = models.IntegerField(null=True,blank=True)
    employeeId = models.CharField(max_length=300, null=True,blank=True)

    def __str__(self):
        return self.user.first_name

class Category(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    description = models.CharField(max_length=1000,null=True, blank=True)
    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    price = models.FloatField(default=0.00)
    availableQuantity = models.IntegerField(default=0, null=True, blank=True)
    description = models.CharField(max_length=1000,null=True, blank=True)  
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    cafe = models.ForeignKey(Cafe,on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

# class Cart(models.Model):
#     foodItem = models.ManyToManyField(FoodItem, null=True, blank=True)
#     description = models.CharField(max_length=1000,null=True, blank=True)
#     category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
#     customer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self):
#         return self.name

class Order(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(User,related_name='customer',on_delete=models.CASCADE, null=True, blank=True)
    cafe = models.ForeignKey(Cafe, related_name='cafe',on_delete=models.CASCADE, null=True, blank=True)
    foodItems = models.ManyToManyField(FoodItem, null=True, blank=True)
    order_status = models.IntegerField(default=1, choices=ORDER_STATUS)
    price = models.FloatField(default=0.00)
    note =  models.CharField(max_length=1000,null=True, blank=True)
    def __str__(self):
        return self.customer.first_name + "_" + self.foodJoint.first_name

