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
    
    url(r'^getCompanies/$', views.getCompanies, name="getCompanies"),
    url(r'^getCompany/(?P<companyId>\d+)/$', views.getCompany, name="getCompany"),


    url(r'^addItem/$', views.addItem, name="addItem"),
    url(r'^orderItems/$', views.orderItems, name="orderItems"),

]
