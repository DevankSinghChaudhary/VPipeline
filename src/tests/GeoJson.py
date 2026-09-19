import requests

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={
        "q": "India Gate, New Delhi",
        "format": "jsonv2",
        "limit": 1,
    },
    headers={"User-Agent": "VPipeline/0.1"},
    timeout=10,
)

print(response.status_code)
print(response.text)

data = response.json()
print(data)
