from datetime import datetime, timezone
import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"


def summarize_emails(emails):
    if not emails:
        return "No emails in the last 24 hours."

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%A, %B %d, %Y")

    email_texts = []
    for e in emails:
        email_texts.append(f"From: {e['from']}\nSubject: {e['subject']}\nPreview: {e['snippet']}")
    email_block = "\n---\n".join(email_texts)

    prompt = f"""You are a personal email assistant. Below are emails received in the last 24 hours ({date_str}).

Summarize them into a brief digest. Group by importance. Highlight anything urgent (deadlines, billing, action items). End with a one-sentence overall take.

Emails:
{email_block}

Digest:"""

    try:
        resp = httpx.post(
            OLLAMA_URL,
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
    except Exception as e:
        return f"Error contacting Ollama: {e}"


