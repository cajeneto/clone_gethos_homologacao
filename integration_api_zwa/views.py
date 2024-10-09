from django.shortcuts import render
import http.client
import json

# Create your views here.


""" 
conn = http.client.HTTPSConnection("api.z-api.io")

payload = "{\"phone\": \"5582991326715\", \"message\": \"Welcome to *Z-API*\"}"

headers = { 'client-token': "F1134eeca2cf748be89c29ca317faf019S" }

conn.request("POST", "/instances/3D647FFC69B400D738AF3E0DE9D9E9B8/token/1AEDCE4DDED8615D8D50B80E/send-text", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))




# cliente token (segurança) {F1134eeca2cf748be89c29ca317faf019S}
 """