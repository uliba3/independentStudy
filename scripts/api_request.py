import requests

response = requests.get("http://localhost:8000/search", params={"query": "I want to make a girlfriend"})
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Could not decode JSON response")
