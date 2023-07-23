import requests

endpoint = 'http://localhost:8000/api/products/'

data = {
    "title": "this field is completed x4"
}

get_response = requests.post(endpoint, data)

print(get_response.json())
