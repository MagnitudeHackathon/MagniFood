from django.conf.urls import url, include
from . import views
from django.contrib.auth.models import User
from app.models import *
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^signup/$', views.signup_view, name="signup"),
    
    url(r'^getItems/$', views.getItems, name="getItems"),
    url(r'^getItem/(?P<itemId>\d+)/$', views.getItem, name="getItem"),

    url(r'^getCafeterias/$', views.getCafeterias, name="getCafeterias"),
    url(r'^getCafeteria/(?P<cafeteriaId>\d+)/$', views.getCafeteria, name="getCafeteria"),

    url(r'^getCafes/$', views.getCafes, name="getCafes"),
    url(r'^getCafe/(?P<cafeId>\d+)/$', views.getCafe, name="getCafe"),
    
    url(r'^addCafe/$', views.addCafe, name="addCafe"),
    url(r'^removeCafe/$', views.removeCafe, name="removeCafe"),
    url(r'^updateCafe/$', views.updateCafe, name="updateCafe"),
    
    url(r'^getCompanies/$', views.getCompanies, name="getCompanies"),
    url(r'^getCompany/(?P<companyId>\d+)/$', views.getCompany, name="getCompany"),


    url(r'^addIngredient/$', views.addIngredient, name="addIngredient"),

    url(r'^addItem/$', views.addItem, name="addItem"),
    url(r'^removeItem/$', views.removeItem, name="removeItem"),
    url(r'^updateItem/$', views.updateItem, name="updateItem"),

    url(r'^orderItems/$', views.orderItems, name="orderItems"),
    url(r'^getOrders/$', views.getOrders, name="getOrders"),

]
