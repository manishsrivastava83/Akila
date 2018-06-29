#Create a business account 
curl -v -X POST -T createBusinessAct.json "http://10.1.22.29:3000/portal/v1/accounts"

#Simulate a sms receive from twillio
curl -v -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "User-Agent: TwilioProxy/1.1" -d @sms_from_twilio.txt "http://10.1.22.29:3000/welcome/sms/reply"
