# AI-CV-Tailor

AI-CV-Tailor is an automated, ATS-aware resume tailoring system that
generates role-optimized CVs and downloadable PDFs via a Streamlit UI.

## Features

- ATS Analysis
- Role Classification
- Dynamic Experience Ranking
- Dynamic Project Ranking
- Dynamic Bullet Tailoring
- PDF Generation
- Streamlit UI

## Architecture

Job Description
↓
ATS Analysis
↓
Role Classification
↓
Experience Ranking
↓
Project Ranking
↓
Bullet Tailoring
↓
PDF Generation

## Screenshots

Placeholders for screenshots (add images/screenshots in `docs/` or `assets/`).

## Installation (local)

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
streamlit run src/app.py
```

The app will be available at `http://localhost:8501` by default.

## Deployment (Streamlit Community Cloud)

1. Push your repository to GitHub (branch `feature/streamlit-ui` or `main`).
2. Go to https://streamlit.io/cloud and create a new app.
3. Connect your GitHub repo and select the branch.
4. Set the app entry point to: `src/app.py`.
5. (Optional) set environment variables or Advanced settings in Streamlit Cloud.

Streamlit Cloud will install dependencies from `requirements.txt` and
expose the app on a public URL.

## Deployment (Render / Railway)

These platforms also support Python/Streamlit apps. Configure service to run:

```bash
streamlit run src/app.py
```

and point the platform to the repository root. Ensure `requirements.txt` is
present so dependencies are installed.

## Streamlit UI Improvements

- Better page title and short app description
- ATS Analysis expander (matched/missing keywords, tailoring strategy)
- Loading spinner while generating CV
- Success notification after PDF creation
- Footer message on the UI

## Optional

There is an expandable "View ATS Analysis" panel showing detected role,
ATS score, matched keywords and missing keywords.

## Validation

To validate locally:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

The app is designed to be compatible with Streamlit Community Cloud. Ensure
the entrypoint is set to `src/app.py` when configuring the deployment.

## License

MIT
