import os
import requests
from dotenv import load_dotenv

load_dotenv()


def linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/32f3c85b9513994c572613f2c8b376b633bfc43f/eden-marco-scrapin.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return None

        data = response.json().get("person")
        if not data:
            print("No person data found:", response.json())
        return data



if __name__ == "__main__":
    print(
        linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/"
        ),
    )