# Bebeğim- Gebelik Takip

Bu repo, gebelik takibi odakli bir web frontend (Vite + React + TypeScript) ve FastAPI backend yapisini icerir. Frontend tarafi su anda mock/sabit veri ile calisacak sekilde entegre edilmistir.

## Klasor Yapisi
- `frontend`: Vite + React + TypeScript tabanli web uygulamasi
- `backend`: FastAPI tabanli API (auth, dashboard, health logs, counters, library, forum, rapor)

## Frontend Calistirma (Windows)
1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Tarayicida terminalde yazan adresi acin (genelde `http://localhost:5173`)


### Frontend Build
- `npm run build`
- Cikti klasoru: `frontend/dist`

## Backend Calistirma (Windows)
1. `cd backend`
2. `python -m venv .venv`
3. `.venv\\Scripts\\activate`
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

## Testler
- Backend: `pytest tests`
- Frontend (varsa): `cd frontend && npm run test`


