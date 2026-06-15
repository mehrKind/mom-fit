
# Replace with your Firebase server key


# Replace with the device token you want to send to
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
import json
SERVER_KEY = "BI257cWytkOadvUcID4wJN6W_XvLf0xTs39WjL5ClSgurQkf6SGjwGE3DslIEwwyOmQ0_2MZw0DSClHloMoB5f4 "
# ==========================
# CONFIGURATION
# ==========================
SERVICE_ACCOUNT_FILE = "./mom-fit-94c88-firebase-adminsdk-fbsvc-7664a9ecb9.json"  # Downloaded JSON from Firebase
PROJECT_ID = "mom-fit-94c88"  # Your Firebase project ID
DEVICE_TOKEN = "fVVgWNEpRNKwtQ9LC8Xivj:APA91bF76wMckoOUg66qNCq18rgEPAZIGpw1L_-mi_D8pQQUVtD0DXOmRHfeVQvAsQZjK8OTWcU00H11DLp_jMZ-fZ4XhHm46zx6BBV99jjDb7-jLqeuExc"
# DEVICE_TOKEN = "eUAO6CUZSBSPHkI2DFoEw9:APA91bE42lVTISBVP1-v_L-owWhoSzkc-3SShUyH_51Zjzw2QTd2nXpULBranWCWla0sd-LZY6hdu7RO2ZRNLTc899ouXxpfT4GnLUxNNceHh9TcKgGEgaw"


# ==========================
# 1️⃣ Generate OAuth2 Access Token
# ==========================
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/firebase.messaging"]
)

request = google.auth.transport.requests.Request()
credentials.refresh(request)  # refresh and get access token
access_token = credentials.token
print("Access token acquired ✅")

# ==========================
# 2️⃣ FCM v1 API endpoint
# ==========================
FCM_ENDPOINT = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

# ==========================
# 3️⃣ Notification payload
# ==========================
payload = {
    "message": {
        "token": DEVICE_TOKEN,
        "notification": {
            "title": "MoM Fit",
            "body": "صبح عالی پرتقالی"
        },
        "data": {
            "extra_info": "Optional custom data"
        }
    }
}

# ==========================
# 4️⃣ Send POST request
# ==========================
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json; UTF-8",
}

response = requests.post(FCM_ENDPOINT, headers=headers, json=payload)

# ==========================
# 5️⃣ Check response
# ==========================
print("Status Code:", response.status_code)
print("Response:", response.text)
