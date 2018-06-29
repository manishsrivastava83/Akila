import tornado.web
import base64
import logging
import re
from tornado import gen, web, httpclient
from tornado.web import URLSpec as url
from tornado.web import stream_request_body
from tornado import httputil
from datetime import datetime
from LoggerClient import LoggerClient
from RedisSessionStore import RedisSessionStore
from DbInterface import DBConnection 
from DbInterface import QueryGateway 
import json
import ast 
import uuid

#self.statementMap["insert_business_accounts"] = "INSERT INTO business_accounts (oid_index,businessAccountUID,businessEntityName,EIN,firstName,middleName,lastName,emailID,password,contactNumber,address,city,country,zipCode) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') "
def createAccount(accountInfo):
    print("firstName is -->",accountInfo['firstName'])
    queryGateway=QueryGateway()
    contactInfo = accountInfo['contactInfo']
    print("contact number is -->",contactInfo['contactNumber'])
    queryGateway.insertBAN(('1','12345','testCompany','NULL',accountInfo['firstName'],'NULL',accountInfo['lastName'],accountInfo['emailId'],accountInfo['password'],contactInfo['contactNumber'],'11','12','13','14'))
    #queryGateway.insertBAN(( str(1),str(uuid.uuid1()),str(1),str(uuid.uuid1()),str(1),str(uuid.uuid1()),str(1),str(uuid.uuid1()),str(1),str(uuid.uuid1()),str(1),str(uuid.uuid1()),str(1),str(uuid.uuid1()) ))
    #queryGateway.insertBAN(( str(1),str(uuid.uuid1())))

class AccountsEndPoint(tornado.web.RequestHandler):

    def handle_request(response):
        if response.error:
            print("here I am ")
            print("Error:", response.error)
        else:
            print(len(response.body))

    def head(self,url):
        print(self.request.headers)

    @web.asynchronous
    @gen.coroutine
    def get(self,url):
        print("handling GET requst from Twillio")
    
    @web.asynchronous
    def prepare(self):
        print("AccountsEndPoint::handling requst from Twillio printing Headers")
        #print(self.request.headers)
    
    @web.asynchronous
    def on_finish(self):    
        print("AccountsEndPoint:on_finish")

    @web.asynchronous
    @gen.coroutine
    def post(self):
        print("AccountsEndPoint: Incoming HTTP POST")
        #print(self.request.body)
        rqstLine = str(self.request.uri)
        print(rqstLine)
        decodedBody = tornado.escape.json_decode(self.request.body)
        print("decodedBody is -->",decodedBody)
        if rqstLine.find("/portal/v1/accounts") != -1:
           print("Request is for account creation")
           accountInfo = decodedBody['accountInfo']
           createAccount(accountInfo)
        else :
            print("not matched")
        queryGateway=QueryGateway()
        #queryGateway.insertBAN({'1','2','3','4','5','6','7','8','9','10','11','12','13','14'})
        self.finish()
