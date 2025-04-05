import os 
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
def linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/Sam-200051806/c891f26bc9438bdb9ee8fa79f76826b5/raw/876c370d6ca9960518e46bdcea4a786f76a5c52f/kartikey.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
        return response.json()
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey" : os.environ["SCRAPIN_API_KEY"],
            "LinkedInUrl": linkedin_profile_url,
        }   
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )
        data = response.json().get("person")
        return data


if __name__ == "__main__":
    print(
        linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/kartikey-sangal-752567301/",
            mock=True,
        )
    )