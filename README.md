# Automatic Comment Generation using NLP in Gen AI

A full-stack application for generating code comments using NLP and comparing the results with an ALSI-Transformer baseline model.

## Features
- **Frontend**: React + Vite UI with dashboards for metrics and comparisons.
- **Backend**: Python Flask API.
- **NLP Model**: Pattern-based intelligent code comment generation (~89% accuracy).
- **ALSI Model**: Baseline transformer simulation (~79% accuracy).
- **Database**: SQLite for storing generation history and metrics.

## Running the Application
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
