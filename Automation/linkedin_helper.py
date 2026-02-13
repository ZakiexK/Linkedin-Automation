import os
import requests

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
URN = os.getenv("LINKEDIN_URN")  # your LinkedIn user or org URN

BASE_URL = "https://api.linkedin.com/v2"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json"
}

def register_upload():
    url = f"{BASE_URL}/assets?action=registerUpload"
    body = {
        "registerUploadRequest": {
            "owner": URN,
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [
                {
                    "identifier": "urn:li:userGeneratedContent",
                    "relationshipType": "OWNER"
                }
            ],
            "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
        }
    }
    r = requests.post(url, headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()

def upload_image(upload_url, image_path):
    with open(image_path, "rb") as f:
        r = requests.put(upload_url, data=f, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
        r.raise_for_status()

def create_post_with_image(post_text, image_urn):
    url = f"{BASE_URL}/ugcPosts"
    body = {
        "author": URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {"text": "Auto-generated post"},
                        "media": image_urn,
                        "title": {"text": "Generated Image"}
                    }
                ]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    r = requests.post(url, headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()

def post_text_with_image(post_text, image_path):
    upload_info = register_upload()
    upload_url = upload_info["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    image_urn = upload_info["value"]["asset"]

    upload_image(upload_url, image_path)

    return create_post_with_image(post_text, image_urn)
