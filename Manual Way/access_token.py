import requests
import os
from dotenv import load_dotenv

load_dotenv()

# SECURITY: Never hardcode credentials! Use environment variables instead
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE")
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# Step 1: Authorization link (open this in browser manually once)
print(f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=w_member_social")

# Step 2: After approving, LinkedIn redirects with a `code` in the URL
# SECURITY: Never commit authorization codes! Paste your code here when running locally
code = "PASTE_YOUR_AUTHORIZATION_CODE_HERE"

# Step 3: Exchange code for access token
# Uncomment when ready to use
# resp = requests.post(TOKEN_URL, data={
#     "grant_type": "authorization_code",
#     "code": code,
#     "redirect_uri": REDIRECT_URI,
#     "client_id": CLIENT_ID,
#     "client_secret": CLIENT_SECRET
# })

# print(resp.json())
