# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User

from .models import *

class ProfleInline(admin.TabularInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfleInline]
    list_display = ["username","first_name", "last_name", "email", "is_active", "is_staff","pk"]
    list_filter = ["is_active", "is_staff"]
    list_editable = ["is_active", "is_staff"]

admin.site.register(Address)
admin.site.register(Cafeteria)
admin.site.register(Cafe)
admin.site.register(Company)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(StoreHouse)
admin.site.register(Ingredients)
admin.site.register(IngridientDetail)
