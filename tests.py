# #System Tests
# from urllib import urlencode
# import urllib2
# import os
# import json
# cookie=""
# def http_post(url, data, name):
#     #post = urlencode(data)
#     print url,data,name
#     global cookie
#     if(name == "login" or name == "removeCafe"):
#         req = urllib2.Request(url, json.dumps(data))
#         response = urllib2.urlopen(req)
#         cookie = response.headers.get('Set-Cookie')
#     else:
#         req2 = urllib2.Request(url, json.dumps(data))
#         req2.add_header('cookie', cookie)
#         response = urllib2.urlopen(req2)

#     return response.read()


# def http_get(url):
#     print url
#     req = urllib2.Request(url)
#     response = urllib2.urlopen(req)
#     return response.read()



# addressHosted = "10.54.3.6:9000/"

# endPoints = {
#    "Post" : ["http://10.54.3.6:9000/signup/","http://10.54.3.6:9000/login/","http://10.54.3.6:9000/orderItems/","http://10.54.3.6:9000/addCafe/","http://10.54.3.6:9000/addItem/"],
#    "Get"  : ["http://10.54.3.6:9000/getItems/","http://10.54.3.6:9000/getItem/1/","http://10.54.3.6:9000/logout/", "http://10.54.3.6:9000/getCafes/", "http://10.54.3.6:9000/getCafe/1/",
#    "http://10.54.3.6:9000/getCafeterias/","http://10.54.3.6:9000/getCafeteria/1/","http://10.54.3.6:9000/getCompanies/","http://10.54.3.6:9000/getCompany/1/"],
#    "Delete" : ["http://10.54.3.6:9000/removeCafe/"]
# }

# #os.chdir("..")
# os.chdir("Tests")
# print os.getcwd()
# for key in endPoints.iterkeys():
    
#     if key == "Post":
#         for locations in endPoints[key]:
#             location = locations.split("/")
#             locationFile = location[len(location)-2]
#             d = {}
#             f = open(locationFile+".json",'r')
#             d = json.loads(f.read())
#             print http_post(locations,d,locationFile)
#             print
        
#     if key == "Get":
#         for locations in endPoints[key]:
#             print http_get(locations)
#             print

#     if key == "Delete":
#         for locations in endPoints[key]:
#             print http_post(locations,{},location[len(location)-2])
#             print




#UnitTest

from django.test import TestCase
import urllib2
import unittest
link_types= ['application/json', 'application/xml']

def is_feed(url):
    print url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.getcode()


from django.test.testcases import TestCase

class IsFeed(unittest.TestCase):
    """Tests the functionality of utility.is_feed
    by getting various well-known good feeds and
    making sure they validate"""

    def test_is_feed_atom(self):
        url = "http://10.54.3.6:9000/getItems/"
        print is_feed(url)
        self.assertEqual(200, is_feed(url))