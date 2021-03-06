#!/usr/bin/env python3

import json
import requests
import time

pepurl = "http://localhost:9999/"
startEvaluation = "start"
finish = "finish"
status = "status"

#start evaluation

print("*****Start evaluation*****")

response = requests.post(pepurl + startEvaluation)
assert(response.status_code == 200)
messageId = str(response.content.decode('utf-8'))
assert('ID:' in messageId)
print(messageId)

print("*****Wait 10 seconds*****")

flowResponse = ''
for i in range(0,10) : 
    time.sleep(1)

    print("Get flow status" + messageId)

    payload='messageId=' + messageId

    response = requests.get(pepurl + status, params=payload)
    assert(response.status_code == 200)
    flowResponse = response.content.decode('utf-8')


print(flowResponse)

statusObject = json.loads(flowResponse)

#"status": "STARTACCESS_PERMIT"
assert(statusObject['status'] == 'STARTACCESS_PERMIT')
assert(len(statusObject['sessionId']) >  0)

print("*****Finish*****" + statusObject['sessionId'])
headers = {'Content-type': 'text/plain'}
response = requests.post(pepurl + finish, headers=headers,data=statusObject['sessionId'])
assert(response.status_code == 200)

for i in range(0,20) :
    time.sleep(1)

    print("Get flow status" + messageId)

    payload='messageId=' + messageId

    response = requests.get(pepurl + status, params=payload)
    assert(response.status_code == 200)
    flowResponse = response.content.decode('utf-8')


print(flowResponse)

statusObject = json.loads(flowResponse)

#"status": "STARTACCESS_PERMIT"
assert(statusObject['status'] == 'ENDACCESS_PERMIT')

print("*****END*****")
