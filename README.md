# Landing Page Chatbot — Founder-ready summary

This repository contains a minimal landing-page chatbot composed of:

- `main.py` — FastAPI backend that forwards chat completion requests to the Groq API.
- `app.py` — Streamlit frontend that provides a simple chat UI and calls the FastAPI backend.
- `.env.example` — Example environment variables.


## How it works (short)

1. The Streamlit UI (`app.py`) collects a user message and calls the FastAPI API at `/api/chat`.
2. The FastAPI backend (`main.py`) validates the input, builds a short system prompt (Nova the assistant), and calls the Groq client to create a chat completion.
3. The assistant reply is returned to Streamlit and shown in the UI.


## Requirements

- Python 3.10+
- See `requirements.txt` for runtime packages (FastAPI, Uvicorn, Streamlit, Groq, python-dotenv, etc.).


## Quick start (local/demo)

1. Copy the example env file and set your Groq API key:

   cp .env.example .env
   # Edit .env and set GROQ_API_KEY

2. Install dependencies (ideally in a virtualenv):

   python -m pip install -r requirements.txt

3. Start the FastAPI backend (development):

   uvicorn main:app --reload --port 8000

4. Start the Streamlit UI in another terminal:

   streamlit run app.py

5. Open http://localhost:8501 in a browser and interact with Nova.


## Founder demo talking points

- The assistant is branded "Nova" and uses a small system prompt to stay concise and friendly.
- The architecture separates UI and API: Streamlit handles the frontend while FastAPI handles model calls. This makes it easy to replace the UI or scale the API independently.
- Readiness checks: FastAPI exposes `/health` for uptime/health probes.
- Security/ops: We keep the API key outside the code in environment variables.


## Production notes & next steps

1. Secrets: Move GROQ_API_KEY to a secret manager (AWS Secrets Manager, GCP Secret Manager, or Vault).
2. Deploy the API behind a process manager (gunicorn + uvicorn workers) or an ASGI platform. Add HTTPS/TLS, a load balancer, and basic auth/rate limiting.
3. Observability: Add structured logs, request tracing, and metrics (Prometheus) + alerting.
4. Safety & moderation: Add input sanitization, moderation filters, and throttling to protect cost and prevent abuse.
5. Tests: Add unit tests for endpoints and e2e tests for the critical chat path.


## Files changed in this update

- `main.py`: added logging, CORS, startup validation (fail fast if GROQ_API_KEY missing), `/health` endpoint, and improved error handling.
- `app.py`: made the backend URL configurable and improved error messages/timeouts.
- `.env.example`: new file documenting environment variables.
- `README.md`: this founder-ready summary and run instructions.


If you'd like, I can also:
- Add a Dockerfile and docker-compose for quick deploy/demo.
- Add a GitHub Actions workflow to run linting and start the app for smoke tests.
- Add a simple unit test or minimal integration test that mocks the Groq client.
