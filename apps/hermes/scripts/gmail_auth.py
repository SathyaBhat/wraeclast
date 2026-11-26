#!/usr/bin/env python3
"""One-time Gmail read-only authorisation. Run this yourself in a terminal; do not paste the result into chat."""
import os, sys
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # redirect is http://localhost; no network hop, so safe
from google_auth_oauthlib.flow import Flow

SECRETS = "/opt/data/secrets"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT = "http://localhost:1/"

flow = Flow.from_client_secrets_file(f"{SECRETS}/gmail_client.json", scopes=SCOPES, redirect_uri=REDIRECT)
url, _ = flow.authorization_url(access_type="offline", prompt="consent")
print("1. Open this URL in your browser and approve read-only access:\n\n" + url + "\n")
print("2. Your browser will then fail to load http://localhost:1/... That is expected.")
print("   Copy the full URL from the address bar and paste it below.\n")
resp = input("Redirected URL: ").strip()
flow.fetch_token(authorization_response=resp)
with open(f"{SECRETS}/gmail_token.json", "w") as f:
    f.write(flow.credentials.to_json())
import os; os.chmod(f"{SECRETS}/gmail_token.json", 0o600)
print("Saved token. Scope:", SCOPES[0])
