import requests

url = 'http://localhost:8080/api/vm'
data = {"name": "DevServer", "cpu": 4, "ram": "16GB"}
response = requests.post(url, json=data)
print(response.json())