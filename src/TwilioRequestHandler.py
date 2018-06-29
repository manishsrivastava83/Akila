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
from twilio import twiml
from DbInterface import DBConnection 
from DbInterface import QueryGateway 
import uuid
#from twilio.twiml.messaging_response import MessagingResponse

from twilio.rest import Client
import tornado.escape
import codecs
#import urllib
#from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests 
import dialogflow


#Run below export command before starting python with this file.
#export GOOGLE_APPLICATION_CREDENTIALS="/root/MANISH_TEST/HotelCustomerCare-22423c992106.json"
#Project ID - hotelcustomercare-58ef0
#Service Account - dialogflow-eadhoj@hotelcustomercare-58ef0.iam.gserviceaccount.com
#language_code - en
account_sid="AC30069c06192e660902ed8338c41b6c72"
auth_token="93913de197c658d25fd80ddbe5f76a89"
dialogFlow_project_id ="hotelcustomercare-58ef0"

session_client = dialogflow.SessionsClient()
client=Client(account_sid,auth_token)

#---------------------------------------#
#send SMS using twilio sdk
#---------------------------------------#
def sendMessage(msisdn,text):
	print("sending message to:",msisdn)
	message=client.messages.create(
		to=msisdn,
	 	from_="+12145061189",
		body=text)

	print("sid is",message.sid)


#MariaDB [bot_HR]> select * from hotel_customer where msisdn='12142357247';
#+----+-------------+-----------+------------+----------------------+-------------+
#| id | msisdn      | firstName | lastName   | address              | originCity  |
#+----+-------------+-----------+------------+----------------------+-------------+
#|  1 | 12142357247 | Manish    | Srivastava | 800 West Renner ROad | Delhi,India |
#+----+-------------+-----------+------------+----------------------+-------------+
def getMessageText(msisdn,input_text):
        print("Enter getMessageText")
        print("msisdn is",msisdn)
	#cnx=mysql.connector.connect(**config)
	#cursor = cnx.cursor()
	#query=("select * from hotel_customer where msisdn='")
	#query+=msisdn
	#query+="';"
	#print query
	#cursor.execute(query)
	#for(id,msisdn,firstName,lastName,address,originCity) in cursor:
	#	displayText="Hello !!"
	#	displayText+=firstName
	#	displayText+=input_text		
	#	print displayText
	#cnx.close()
        displayText = input_text
        return displayText

#---------------------------------------#
#take db data against session_id
#switch case on intent_name
#replace macros in fulfillment_text and send sms back to number=session_id
#---------------------------------------#
def handleDialogFlowRsp(session_id,fulfillment_text,intent_name):
	if intent_name=='Send_Welcome_Msg':
		print("Intent is Send_Welcome_Msg")
		returnText = getMessageText(session_id,fulfillment_text)
		sendMessage(session_id,returnText)
	elif intent_name=='Positive_Feedback':
		print("Intent is Positive_Feedback")
		sendMessage(session_id,fulfillment_text)
	elif intent_name=='Negative_Feedback':
		print("Intent is Negative_Feedback")
		sendMessage(session_id,fulfillment_text)
	else:	
		print("Intent is general")
		sendMessage(session_id,fulfillment_text)


#---------------------------------------#
#"""Returns the result of detect intent with texts as inputs.
#Using the same `session_id` between requests allows continuation
#of the conversaion."""
#---------------------------------------#
def detect_intent_texts(session_id, texts, language_code):
	session = session_client.session_path(dialogFlow_project_id, session_id)
	print('Session path: {}\n'.format(session))
	text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)
	query_input = dialogflow.types.QueryInput(text=text_input)
	response = session_client.detect_intent(session=session, query_input=query_input)
	print('=' * 20)
	print('Query text: {}'.format(response.query_result.query_text))
	print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
	print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
	fulfillment_text = response.query_result.fulfillment_text
	intent_name = response.query_result.intent.display_name

	handleDialogFlowRsp(session_id,fulfillment_text,intent_name)




class TwilioRequestHandler(tornado.web.RequestHandler):

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
        self.logger = LoggerClient()
        #print(self.request.headers)
    
    @web.asynchronous
    def on_finish(self):    
        print("TwilioRequestHandler:on_finish")

    @web.asynchronous
    @gen.coroutine
    def post(self):
        #print(self.request)
        LoggerClient().sendLogMessage({self.request,self.request.body});
        #TODO assertion and validation --> Content Length/URL params/Body validation
        twilioRequestBody = parse_qs(str(self.request.body))
        queryGateway=QueryGateway()
        sessionId = str(twilioRequestBody['From'])
        queryGateway.storeMessageFromTwillio((str(uuid.uuid1()),str(twilioRequestBody['From']),str(twilioRequestBody['To']),str(twilioRequestBody['Body']),str(datetime.now()),sessionId))
         
        bodyText = str(twilioRequestBody['Body'])
        sourceNumber = str(twilioRequestBody['From'])
        print("BodyText is ",bodyText)
        print("sourceNumber is ",sourceNumber)
        #bodyText= bodyText[0].encode("utf8")
        #sourceNumber= sourceNumber[0].encode("utf8")
        detect_intent_texts(sourceNumber,bodyText,"en")
        self.finish()
