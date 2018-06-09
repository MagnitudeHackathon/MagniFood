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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(default=2, choices=USER_TYPES)
    date_added = models.DateTimeField(default=timezone.now)
    blockName  = models.CharField(max_length=300, null=True,blank=True)
    floor = models.CharField(max_length=300, null=True,blank=True)
    company = models.CharField(max_length=300, null=True,blank=True)
    contactNumber = models.IntegerField(null=True,blank=True)
    employeeId = models.CharField(max_length=300, null=True,blank=True)

    def __str__(self):
        return self.user.first_name

class Category(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    cost = models.FloatField(default=0.00)
    description = models.CharField(max_length=1000,null=True, blank=True)
    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    price = models.FloatField(default=0.00)
    description = models.CharField(max_length=1000,null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    foodJoint = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    foodItem = models.ManyToManyField(FoodItem)
    description = models.CharField(max_length=1000,null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    foodJoint = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

