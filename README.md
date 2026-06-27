# Email Daily Digest

AI-powered daily email digest in your browser. Fetches the last 24 hours of emails via Gmail API and summarizes them using Ollama (Llama 3.2).

## Project Structure

```
email-summarizer/
├── backend/
│   ├── main.py              # FastAPI server (port 9876)
│   ├── gmail_service.py     # Gmail API client
│   ├── summarizer.py        # Ollama summarization
│   └── requirements.txt
├── extension/
│   ├── manifest.json        # Chrome extension manifest (v3)
│   ├── popup.html           # Popup UI
│   ├── popup.css            # Dark glassmorphism styles
│   ├── popup.js             # Popup logic
│   └── icons/
├── .gitignore
├── generate_icon.py         # Icon generator script
├── register_autostart.ps1   # Scheduled task auto-start
├── start_backend.vbs        # Silent launcher (no console)
└── README.md
```

## Prerequisites

- **Python 3.12+**
- **Ollama** with `llama3.2` pulled: `ollama pull llama3.2`
- **Gmail API credentials** — download `credentials.json` from Google Cloud Console and place it in `backend/`

## Setup

```bash
cd backend
pip install -r requirements.txt
```

On first run, the Gmail API flow will open your browser for authentication.

## Usage

```bash
cd backend
python main.py
```

Open the extension popup from your browser toolbar to see your daily digest.

## Auto-Start (Windows)

**Option A — Registry (recommended):**
```reg
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "EmailDigestBackend" /t REG_SZ /d "pythonw \"C:\email-summarizer\backend\main.py\"" /f
```

**Option B — Scheduled Task:**
```powershell
.\register_autostart.ps1
```

## Tech Stack

- **Backend:** FastAPI, Uvicorn, Google API Client, Ollama
- **Extension:** Manifest V3, vanilla JS
- **UI:** Dark glassmorphism, system tray icon
