import requests
from test import client
#from init_app_db import db
#from models import User

'''
datadict = [{'email' : 'request0@test.com', 'username' : 'request_test', 'password' : 'pass'}]
my_headers = {'Authorization' : 'Bearer {access_token}'}
response_user_signup_post = requests.post("http://127.0.0.1:5000/signup", headers=my_headers, data=str(datadict))
#response_user_signup_post = requests.post("http://127.0.0.1:5000/signup", auth=HTTPBasicAuth({'email' : 'request0@test.com'}, {'username' : 'request_test'}, {'password' : 'pass'}))
print(response_user_signup_post.json, '\n', response_user_signup_post.text)
'''

#response_post_get = requests.get("http://127.0.0.1:5000/posts") print(response_post_get.json, '\n', response_post_get.text)

#response_user_details_get = requests.get("http://127.0.0.1:5000/users") print(response_user_details_get.json, '\n', response_user_details_get.text)

#response_signup = client.post('/signup', data={'email' : 'request0@test.com', 'username' : 'request_test', 'password' : 'pass'})

#response_login = client.post('/login', data={'email' : 'request0@test.com', 'password' : 'pass'})

#response_post_get_unauthorized = client.get('/posts')
#print(response_post_get_unauthorized)

my_headers = {'Content-type': 'application/json', 'Authorization' : 'Bearer VALID TOKEN!!!!!!!!!'} #,'Accept': 'text/plain'
#----response_post_get_authorized = client.get('/posts', headers=my_headers)
#----print(response_post_get_authorized)

##### doesn't work from geany - returns [422 UNPROCESSABLE ENTITY]> {'msg': 'Signature verification 0failed'}, but works from terminal
#response_post_post_authorized = client.put('/posts', json={'title' : 'request0 test', 'body' : 'req0 test'}, headers={'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyNzUwNjk5MSwianRpIjoiNjI2MzkxNGEtMWZhNS00NDViLWIxMjktZDU5OTFkMjU0MjdkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEwIiwibmJmIjoxNjI3NTA2OTkxLCJjc3JmIjoiNDUwNDIwMmEtNzVjYi00ZTY0LWE4NTktYzg5MjQ1MWY3ODU3IiwiZXhwIjoxNjI3NTkzMzkxfQ.m2h1p2iiRrGhOPlAsGE87ODk2hOKMrSL17NVMw4m1dY'})
#print(response_post_post_authorized, response_post_post_authorized.json)


resp_like = client.post('/like', json={'post_id':5, 'like_unlike' : 'like'}, headers=my_headers)
