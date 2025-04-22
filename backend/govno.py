import requests

response = requests.get("https://femin.onrender.com/tracks")
print(response.json())