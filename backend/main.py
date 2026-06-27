import threading
import webbrowser
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gmail_service import fetch_recent_emails
from summarizer import summarize_emails
import pystray
from PIL import Image, ImageDraw

app = FastAPI(title="Email Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/summary")
def get_summary():
    emails = fetch_recent_emails()
    summary = summarize_emails(emails)
    return {"total": len(emails), "summary": summary}


def create_icon():
    img = Image.new("RGB", (64, 64), color=(0, 120, 212))
    draw = ImageDraw.Draw(img)
    draw.ellipse([12, 12, 52, 52], fill=(255, 255, 255))
    draw.rectangle([26, 28, 38, 44], fill=(0, 120, 212))
    return img


def on_open(_):
    webbrowser.open("http://127.0.0.1:9876/api/summary")


def on_exit(icon):
    icon.stop()
    import os
    os._exit(0)


def run_tray():
    icon = pystray.Icon(
        "email_digest",
        create_icon(),
        "Email Digest Backend - Running",
        menu=pystray.Menu(
            pystray.MenuItem("Open API", on_open),
            pystray.MenuItem("Exit", on_exit),
        ),
    )
    icon.run()


if __name__ == "__main__":
    threading.Thread(target=run_tray, daemon=True).start()
    uvicorn.run("main:app", host="127.0.0.1", port=9876, reload=False)
