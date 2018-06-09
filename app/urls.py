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
    url(r'^getItem/(?P<itemId>\d+)/$', views.getItem, name="getItem"),#for cafe
    url(r'^addItem/$', views.addItem, name="addItem"),#for cafe
    url(r'^orderItems/$', views.orderItems, name="orderItems"),# for customer

]
