import requests
import pyotp
import time

data = {"email": "luuktholen@live.nl", "password": "123"}
link = "http://localhost:5000/auth"
response = requests.post(link, json=data)
response = response.json()


secret = "KJYCEQBOLW6BPWK4"
totp = pyotp.TOTP(secret)
totp_code = totp.now()
data = {"password": response["info"], "code": totp_code}
link = "http://localhost:5000/totp"

response = requests.post(link, json=data)
response = response.json()
print(response)