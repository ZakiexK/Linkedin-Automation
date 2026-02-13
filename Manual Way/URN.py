import requests
import os
from dotenv import load_dotenv

load_dotenv()

# SECURITY: Never hardcode access tokens! Use environment variables instead
ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
POST_URL = "https://api.linkedin.com/v2/ugcPosts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

post_data = {
    "author": "urn:li:person:your_profile_id",  # You get this from LinkedIn API
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Automated post using Python 🤖 #CyberSecurity #Automation"
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

# resp = requests.post(POST_URL, headers=headers, json=post_data)
# print(resp.json())

def get_profile_urn(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    data = resp.json()
    return print(data)   # "sub" = user ID in OpenID

get_profile_urn(ACCESS_TOKEN)
