from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# read config value
config_file = open("chatbot/default.json", "r")
root = json.load(config_file)

# global attributes
APP_SECRET = root["appSecret"]
VALIDATION_TOKEN = root["validationToken"]
PAGE_ACCESS_TOKEN = root["pageAccessToken"]

@csrf_exempt
def index(request): 
    if request.method == "GET": 
        print(request.GET)
        if (request.GET["hub.mode"] == "subscribe" and 
            request.GET["hub.verify_token"] == VALIDATION_TOKEN): 
            print("Verification successful")
            return HttpResponse(request.GET["hub.challenge"])
        else: 
            return HttpResponse(403) 
    else: 
        handle_actions(request) 
        return HttpResponse("do nothing") 


def handle_actions(request): 
    body = json.loads(request.body)
    if (body["object"] == "page"): 
        # iterate items
        for pageEntry in body["entry"]: 
            pageId = pageEntry["id"]
            timestamp = pageEntry["time"]
            for messagingEvent in pageEntry["messaging"]: 
                if "optin" in messagingEvent:
                    pass
                elif "message" in messagingEvent:
                    receivedMessage(messagingEvent)
                    pass
                elif "delivery" in messagingEvent:
                    pass
                elif "postback" in messagingEvent:
                    pass
                elif "read" in messagingEvent:
                    pass
                elif "account_linking" in messagingEvent:
                    pass
                else:                 
                    pass

def receivedMessage(event): 
    senderId = event["sender"]["id"]
    recipientId = event["recipient"]["id"]
    timeOfMessage = event["timestamp"]
    message = event["message"]

    #isEcho = message["is_echo"]
    #messageId = message["mid"]
    #appId = message["app_id"]
    #metaData = message["metadata"]
    messageText = message["text"] 
    if (messageText): 
        if messageText == "hi" or "hello": 
            sendHiMessage(senderId)
        else: 
            sendByeMessage(senderId)

def sendHiMessage(recipientId):
    msg = { 
        "recipient": {
            "id": recipientId
        }, 
        "message": {
            "text": "Hello World!!"
        } 
    } 
    print("recipient is %s" % recipientId)
    callSendAPI(msg)

def sendByeMessage(senderId):
    pass

def callSendAPI(msgData): 
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                params={"access_token": PAGE_ACCESS_TOKEN},
                data=json.dumps(msgData), 
                headers={'Content-type': 'application/json'})
    print(r.status_code)
    print(r.content)
