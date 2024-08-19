import requests

url = "http://localhost:8000/detect/"

files = {'file': open('input.jpeg', 'rb')}

target_classes = 'person,car'
data = {'target_classes': target_classes}

response = requests.post(url, files=files, data=data)

print(response.json())
