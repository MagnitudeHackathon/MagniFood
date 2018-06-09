from __future__ import unicode_literals


from django.db import models
from django.utils import timezone

# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from MagniFood import settings

USER_TYPES = (
    (1, "FoodJoint"),
    (2, "Customer")
)

ORDER_STATUS = (
    (1, "Ordered"),
    (2, "Confirmed"),
    (3, "Ready"),
    (4, "Delivered")
)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(default=2, choices=USER_TYPES)
    date_added = models.DateTimeField(default=timezone.now)
    block  = models.CharField(max_length=300, null=True,blank=True)
    floor = models.CharField(max_length=300, null=True,blank=True)
    company = models.CharField(max_length=300, null=True,blank=True)
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
    description = models.CharField(max_length=1000,null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    foodJoint = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    availableQuantity = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    foodItem = models.ManyToManyField(FoodItem, null=True, blank=True)
    description = models.CharField(max_length=1000,null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(User,related_name='customer',on_delete=models.CASCADE, null=True, blank=True)
    foodJoint = models.ForeignKey(User, related_name='foodJoint',on_delete=models.CASCADE, null=True, blank=True)
    foodItems = models.ManyToManyField(FoodItem, null=True, blank=True)
    order_status = models.IntegerField(default=1, choices=ORDER_STATUS)
    price = models.FloatField(default=0.00)
    note =  models.CharField(max_length=1000,null=True, blank=True)
    def __str__(self):
        return self.customer.first_name + "_" + self.foodJoint.first_name

