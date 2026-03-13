from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from groq import Groq
import groq

# Load environment variables from .env (if present)
load_dotenv()

# Basic configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
# Optional comma-separated fallback models to try if the primary model is decommissioned
GROQ_FALLBACK_MODELS = [m.strip() for m in os.getenv("GROQ_FALLBACK_MODELS", "").split(",") if m.strip()]

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("landing-chatbot")

# Setup FastAPI
app = FastAPI(title="Landing Page Chatbot API")

# Allow requests from the local Streamlit UI by default; override in env for production
frontend_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in frontend_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request/response models
class ChatRequest(BaseModel):
    user_message: str


class ChatResponse(BaseModel):
    reply: str


SYSTEM_PROMPT = (
    """You are 'Nova', a friendly, enthusiastic, and highly helpful AI assistant for our product's landing page. "
    "Your primary goal is to welcome visitors, answer their queries clearly and concisely, highlight the benefits of our product/service, "
    "and gently encourage them to sign up or get in touch. Keep answers brief (1-3 sentences) and conversational. If unsure, offer to connect to a human agent."""
)


@app.on_event("startup")
async def startup_event():
    # Validate critical config and initialize the Groq client
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        logger.error("GROQ_API_KEY is not set or invalid. Set GROQ_API_KEY in environment or .env.")
        # Raising here will prevent the app from starting; that's desirable in production
        raise RuntimeError("Missing GROQ_API_KEY")

    try:
        app.state.groq_client = Groq(api_key=GROQ_API_KEY)
        logger.info("Groq client initialized")
    except Exception:
        logger.exception("Failed to initialize Groq client")
        raise


@app.get("/health")
async def health():
    """Simple health endpoint for readiness checks."""
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Create a chat completion via Groq and return the assistant reply.

    This endpoint validates inputs, delegates to the Groq client saved on app.state, and logs unexpected errors.
    """
    if not request.user_message or not request.user_message.strip():
        raise HTTPException(status_code=400, detail="user_message cannot be empty")

    client = getattr(app.state, "groq_client", None)
    if client is None:
        logger.error("Groq client is not initialized")
        raise HTTPException(status_code=503, detail="Service unavailable")

    try:
        def _call_model(model_name: str):
            return client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": request.user_message},
                ],
                model=model_name,
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("MAX_TOKENS", "200")),
            )

        # First attempt with configured model
        try:
            chat_completion = _call_model(GROQ_MODEL)
        except groq.BadRequestError as bre:
            # The Groq client returns a BadRequestError for things like decommissioned models.
            msg = str(bre)
            logger.warning("Groq BadRequestError when calling model %s: %s", GROQ_MODEL, msg)

            # If the model was decommissioned, try fallbacks if provided
            if ("decommission" in msg) or ("model_decommissioned" in msg) or ("decommissioned" in msg):
                if GROQ_FALLBACK_MODELS:
                    logger.info("Attempting fallback models: %s", GROQ_FALLBACK_MODELS)
                    last_exc = None
                    for fb_model in GROQ_FALLBACK_MODELS:
                        try:
                            chat_completion = _call_model(fb_model)
                            logger.info("Fallback model %s succeeded", fb_model)
                            break
                        except Exception as e:
                            logger.exception("Fallback model %s failed", fb_model)
                            last_exc = e

                    else:
                        # No fallback succeeded
                        logger.error("All fallback models failed for request")
                        raise HTTPException(status_code=502, detail="Downstream model error: all fallback models failed")
                else:
                    logger.error("Primary model appears decommissioned and no fallbacks configured")
                    raise HTTPException(status_code=502, detail=("Downstream model decommissioned. Set GROQ_MODEL to a supported model "
                                                                   "or configure GROQ_FALLBACK_MODELS in the environment."))
            else:
                logger.exception("BadRequestError from Groq API not related to decommissioning")
                raise HTTPException(status_code=502, detail="Downstream service error")

        # Defensive access: ensure expected fields exist
        reply = ""
        try:
            reply = chat_completion.choices[0].message.content
        except Exception:
            logger.exception("Unexpected response shape from Groq API: %s", getattr(chat_completion, "__dict__", str(chat_completion)))
            raise HTTPException(status_code=502, detail="Downstream service error")

        return ChatResponse(reply=reply)

    except HTTPException:
        # re-raise HTTPExceptions we intentionally raised above
        raise
    except Exception:
        logger.exception("Unhandled exception in chat endpoint")
        # Return a safe, generic error message to the client
        raise HTTPException(status_code=500, detail="Internal server error")
