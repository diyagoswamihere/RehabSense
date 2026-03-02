import requests
import json

# Test login endpoint
url = "http://localhost:5000/login"
data = {
    "patient_id": "1D55PL6",
    "password": "newp@117789"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
