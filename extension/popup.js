const BACKEND_URL = "http://127.0.0.1:9876/api/summary";

const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const resultEl = document.getElementById("result");
const metaEl = document.getElementById("meta");
const summaryEl = document.getElementById("summary-text");
const refreshBtn = document.getElementById("refresh-btn");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

function showLoading() {
  loadingEl.classList.remove("hidden");
  errorEl.classList.add("hidden");
  resultEl.classList.add("hidden");
}

function showError(msg) {
  loadingEl.classList.add("hidden");
  errorEl.classList.remove("hidden");
  resultEl.classList.add("hidden");
  errorEl.textContent = msg;
}

function showResult(total, summary) {
  loadingEl.classList.add("hidden");
  errorEl.classList.add("hidden");
  resultEl.classList.remove("hidden");

  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  metaEl.textContent = `${today} — ${total} email${total !== 1 ? "s" : ""}`;
  summaryEl.textContent = summary;
}

function setConnected(ok) {
  statusDot.className = ok ? "connected" : "";
  statusText.textContent = ok ? "connected" : "offline";
}

async function fetchSummary() {
  showLoading();
  setConnected(false);

  try {
    const resp = await fetch(BACKEND_URL, { signal: AbortSignal.timeout(15000) });
    if (!resp.ok) {
      throw new Error(`Server returned ${resp.status}`);
    }
    const data = await resp.json();
    showResult(data.total, data.summary);
    setConnected(true);
  } catch (err) {
    if (err.name === "TimeoutError") {
      showError("Request timed out. Is the backend running?\n\nRun: python main.py\nin C:\\email-summarizer\\backend\\");
    } else if (err.message.includes("fetch")) {
      showError("Cannot reach the backend server.\n\nMake sure it's running:\n  cd C:\\email-summarizer\\backend\n  python main.py");
    } else {
      showError(`Error: ${err.message}`);
    }
  }
}

refreshBtn.addEventListener("click", fetchSummary);
document.addEventListener("DOMContentLoaded", fetchSummary);
