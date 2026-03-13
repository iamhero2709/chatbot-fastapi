# 🤖 Nova — Landing Page Chatbot

A production-ready landing-page chatbot built with **FastAPI** and **Streamlit**, powered by **Groq LLMs**. Nova greets visitors, answers product questions, and guides them toward conversion — all in a clean, conversational UI.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?logo=streamlit&logoColor=white)](https://chatbot-fastapi-c84ddkczwdkgtmvwfqjuf2.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![CI](https://github.com/iamhero2709/chatbot-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/iamhero2709/chatbot-fastapi/actions/workflows/ci.yml)

---

## 🚀 Live Preview

**[👉 Try Nova live on Streamlit Cloud](https://chatbot-fastapi-c84ddkczwdkgtmvwfqjuf2.streamlit.app/)**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **AI-Powered Chat** | Natural conversation via Groq-hosted LLMs (default: `llama3-8b-8192`) |
| **Quick Replies** | One-click buttons for common questions (pricing, demos, contact) |
| **Separated Architecture** | Streamlit frontend + FastAPI backend — scale or replace each independently |
| **Automatic Model Fallback** | Configurable fallback models if the primary model is decommissioned |
| **Health Endpoint** | `/health` route for uptime monitoring and readiness probes |
| **CORS Configuration** | Configurable allowed origins for cross-origin requests |
| **Startup Validation** | Fail-fast on missing API keys to catch misconfigurations early |
| **Structured Logging** | Configurable log levels for debugging and observability |
| **CI Pipeline** | GitHub Actions workflow for syntax checks and import smoke tests |

---

## 🏗️ Architecture

```
┌──────────────────┐        HTTP POST        ┌───────────────────┐        API call        ┌───────────┐
│   Streamlit UI   │ ──────────────────────▶  │  FastAPI Backend   │ ────────────────────▶  │  Groq API  │
│    (app.py)      │ ◀──────────────────────  │    (main.py)       │ ◀────────────────────  │  (LLM)     │
└──────────────────┘      JSON response       └───────────────────┘     Chat completion    └───────────┘
```

1. **Streamlit UI** (`app.py`) — Collects user messages (free text or quick-reply buttons) and displays the conversation history.
2. **FastAPI Backend** (`main.py`) — Validates input, prepends a system prompt (Nova persona), and calls the Groq chat completion API.
3. **Groq API** — Returns the LLM-generated assistant reply, which flows back through the backend to the UI.

---

## 📁 Project Structure

```
├── app.py              # Streamlit frontend — chat UI with quick replies
├── main.py             # FastAPI backend — /api/chat and /health endpoints
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── streamlit.toml      # Streamlit server configuration
├── DEPLOY.md           # Step-by-step deployment guide (GitHub + Streamlit Cloud)
├── .devcontainer/      # Dev container config for GitHub Codespaces
└── .github/workflows/
    └── ci.yml          # CI pipeline — syntax check & import smoke tests
```

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.10+**
- A **[Groq API key](https://console.groq.com/)** (free tier available)

### 1. Clone & configure

```bash
git clone https://github.com/iamhero2709/chatbot-fastapi.git
cd chatbot-fastapi

cp .env.example .env
# Open .env and set your GROQ_API_KEY
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the FastAPI backend

```bash
uvicorn main:app --reload --port 8000
```

### 4. Start the Streamlit frontend (in a separate terminal)

```bash
streamlit run app.py
```

### 5. Chat with Nova

Open **http://localhost:8501** in your browser and start chatting!

---

## ⚙️ Environment Variables

All configuration is managed through environment variables. See [`.env.example`](.env.example) for a complete template.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ | — | Your Groq API key |
| `GROQ_MODEL` | | `llama3-8b-8192` | Primary LLM model to use |
| `GROQ_FALLBACK_MODELS` | | — | Comma-separated fallback models |
| `FASTAPI_URL` | | `http://localhost:8000/api/chat` | Backend URL used by the Streamlit frontend |
| `FRONTEND_ORIGINS` | | `http://localhost:8501,http://127.0.0.1:8501` | Allowed CORS origins |
| `TEMPERATURE` | | `0.7` | LLM sampling temperature |
| `MAX_TOKENS` | | `200` | Maximum tokens per response |
| `LOG_LEVEL` | | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 🌐 Deployment

The Streamlit frontend is deployed on **[Streamlit Cloud](https://streamlit.io/cloud)** and the FastAPI backend is hosted on **[Railway](https://railway.app/)**.

For a step-by-step guide on pushing to GitHub and deploying to Streamlit Cloud, see **[DEPLOY.md](DEPLOY.md)**.

> **Tip:** Set `GROQ_API_KEY` and other secrets in Streamlit Cloud's **Settings → Secrets** panel instead of committing a `.env` file.

---

## 🔒 Production Considerations

- **Secrets Management** — Move API keys to a secret manager (AWS Secrets Manager, GCP Secret Manager, or HashiCorp Vault).
- **HTTPS & Load Balancing** — Deploy behind a reverse proxy with TLS termination and rate limiting.
- **Observability** — Add structured logging, distributed tracing, and metrics (Prometheus/Grafana).
- **Safety & Moderation** — Add input sanitization, content moderation filters, and per-user throttling.
- **Testing** — Add unit tests for API endpoints and end-to-end tests for the critical chat path.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request
