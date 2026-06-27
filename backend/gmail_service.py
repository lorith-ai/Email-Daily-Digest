import os
import pickle
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.pickle")
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")


def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("gmail", "v1", credentials=creds)


def fetch_recent_emails():
    service = get_service()
    after_ts = int((datetime.now(timezone.utc) - timedelta(hours=24)).timestamp())
    query = f"after:{after_ts}"

    results = service.users().messages().list(userId="me", q=query, maxResults=50).execute()
    messages = results.get("messages", [])

    if not messages:
        return []

    emails = []
    for msg in messages:
        try:
            data = service.users().messages().get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"]).execute()
            headers = {h["name"].lower(): h["value"] for h in data.get("payload", {}).get("headers", [])}
            snippet = data.get("snippet", "")
            emails.append({
                "id": msg["id"],
                "from": headers.get("from", "Unknown"),
                "subject": headers.get("subject", "(No subject)"),
                "date": headers.get("date", ""),
                "snippet": snippet,
            })
        except HttpError:
            continue

    return emails
