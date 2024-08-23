import requests

# API'nin çalıştığı sunucu ve port
URL = "http://localhost:8000/detect"

# Test edilecek dosya ve sınıflar
image_path = "test_image.jpg"
target_classes = ["person", "car"]

files = {"file": open(image_path, "rb")}
data = {"target_classes": target_classes}

response = requests.post(URL, files=files, json=data)

print(response.json())
