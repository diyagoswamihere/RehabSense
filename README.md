# RehabSense

RehabSense is a Flask-based rehabilitation monitoring web app with multilingual UI support and patient report analytics.

## Project Structure

- `backend/app.py` - Flask application and API endpoints.
- `frontend/templates/` - Jinja2 HTML templates for pages and modals.
- `frontend/static/css/style.css` - App style definitions.
- `data/patients/` - Patient JSON records used for dashboard and reports.
- `models/` - Machine learning models used by inference engine.
- `utils/` - Inference and helper utilities.
- `recommendations/engine.py` - Recommendation logic.
- `training/` - Scripts to train model components.

## Features

- Patient login and admin login.
- Patient dashboard with health reports and progress tracking.
- Report-specific prediction and recommendation generation.
- Multilingual support (English + several Indian languages) via in-memory dictionaries.
- Language selector on home page.
- Admin dashboard for listing patient records.

## Requirements

- Python 3.10+ (recommended)
- Flask

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python backend/app.py
```

Open browser at: `http://localhost:5000`

## Language Support

Language can be switched from the drop-down in the home page header. Supported languages include:
- English
- Español
- हिन्दी
- বাংলা
- मराठी
- தமிழ்
- ಕನ್ನಡ
- తెలుగు
- ଓଡ଼ିଆ
- ਪੰਜਾਬੀ
- हरियाणवी
- ગુજરાતી
- भोजपुरी
- اردو

## Patient Login Credentials

- Patient A: ID `1D55PL6`, password `newp@117789`
- Patient B: ID `7D42PL2`, password `neww@342217`

## Notes

- The app currently stores patient data in JSON files under `data/patients`.
- The login and translation behavior are handled in `backend/app.py` with session-based language selection.

## Development

- Add new translation keys in `backend/app.py` within `TRANSLATIONS`.
- Add new templates in `frontend/templates` and use `{{ t('your_key') }}` for translatable text.
- Re-run `python backend/app.py` after changes.
