import requests

url = "https://api.scrapin.io/enrichment/profile"

# Required parameters
headers = {
    "apikey":"sk_92204f724f243324dc1894c8540563b01ef2512c"  # Replace with your actual API key
}

params = {
    "linkedInUrl": "https://www.linkedin.com/in/spyrosigma"  # Replace with actual LinkedIn URL
}

response = requests.request("GET", url, headers=headers, params=params)
print(response.text)