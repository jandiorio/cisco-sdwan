#!/usr/bin/env python

import requests

requests.packages.urllib3.disable_warnings()

HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

auth_url = "https://sandboxsdwan.cisco.com:8443/j_security_check"

credentials = {"j_username": "devnetuser", "j_password": "Cisco123!"}

session = requests.session()

response = session.post(auth_url, headers=HEADERS, data=credentials, verify=False)

print(response.status_code)
print(response.cookies)

url = "https://sandboxsdwan.cisco.com:8443/dataservice/template/feature"

response = session.get(url, verify=False)

print(response.status_code)
# print(response.json())