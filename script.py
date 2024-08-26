import requests

url = 'http://localhost:5001/detect'
data = {
    "image_path": "test.jpg",
    "target_classes": ["person", "car"]
}

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")


try:
    print(response.json())
except ValueError as e:
    print(f"JSON decoding failed: {e}")
