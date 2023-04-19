import json
import requests

headers = {'Accept': 'application/json'}

input_signup = {"email":"ntc-test-123@gmail.com", "username":"1111111111", "password":"1111111111"}
response_signup = requests.post('https://beta-eid-backend.townway.com.tw/accounts/signup', data = input_signup, headers=headers)
print(response_signup.text)
with open("signup.json", "w") as fp:
    json.dump(json.loads(response_signup.text), fp)


input_signin = {"email":"ntc-test-123@gmail.com", "password":"1111111111"}
response_signin = requests.post('https://beta-eid-backend.townway.com.tw/accounts/signin', data = input_signin, headers=headers)
print(response_signin.text)
with open("signin.json", "w") as fp:
    json.dump(json.loads(response_signin.text), fp)
