# How to push this project to GitHub and deploy to Streamlit Cloud

This guide walks you through creating a GitHub repository, pushing this project, and deploying it to Streamlit Cloud.

1) Create a GitHub repository

   - Go to https://github.com/new
   - Choose a repository name (e.g. `landing-chatbot`) and create it.

2) Push your local repo to GitHub (run these locally in the project root):

   git init
   git add --all
   git commit -m "Initial commit: landing chatbot"
   # Replace <YOUR_REMOTE_URL> with the repo URL you created (HTTPS or SSH)
   git remote add origin <YOUR_REMOTE_URL>
   git branch -M main
   git push -u origin main

   If you already have a remote set or credentials configured (SSH key or GitHub CLI), use those instead.

3) Deploy on Streamlit Cloud

   - Go to https://streamlit.io/cloud
   - Sign in with GitHub and authorize access to the repository you pushed.
   - Click "New app", select the repo and branch (main), and set the entrypoint file to `app.py`.
   - Click Deploy.

Notes
- Make sure `.env` isn't committed (we include `.gitignore` to prevent it). Instead set secrets in Streamlit Cloud's Secrets UI for `GROQ_API_KEY` and any other sensitive values.
- In Streamlit Cloud, go to Settings → Secrets and add:

  GROQ_API_KEY=your_groq_api_key_here
  GROQ_MODEL=llama3-8b-8192
  # optionally set GROQ_FALLBACK_MODELS=...

Troubleshooting
- If the app fails to start, check the app logs in Streamlit Cloud and ensure required secrets are set.
- Use the GitHub Actions CI in `.github/workflows/ci.yml` to validate imports before pushing.
