# Bebeğim- Gebelik Takip

Bu repo, gebelik takibi odakli bir web frontend (Vite + React + TypeScript) ve FastAPI backend yapisini icerir. Frontend tarafi su anda mock/sabit veri ile calisacak sekilde entegre edilmistir.

## Klasor Yapisi
- `frontend`: Vite + React + TypeScript tabanli web uygulamasi
- `backend`: FastAPI tabanli API (auth, dashboard, health logs, counters, library, forum, rapor)

## Frontend Calistirma (Windows)
1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Tarayicida terminalde yazan adresi acin
   
## EKRAN GÖRÜNTÜLERİ
<img width="1361" height="734" alt="Image" src="https://github.com/user-attachments/assets/5d4a71eb-5691-4272-a5ac-53b1191763ce" />

<img width="1366" height="723" alt="Image" src="https://github.com/user-attachments/assets/ee24151d-3470-4cfa-934a-ff551aa41af7" />

<img width="1361" height="721" alt="Image" src="https://github.com/user-attachments/assets/ca9272fb-a69e-46fe-aff1-41bba23b38c3" />

<img width="1366" height="727" alt="Image" src="https://github.com/user-attachments/assets/45d27a20-d789-43b5-91b1-7a0a75434848" />

<img width="1366" height="729" alt="Image" src="https://github.com/user-attachments/assets/958639fa-1a11-4e00-bad6-90f1b21f9304" />

<img width="1364" height="728" alt="Image" src="https://github.com/user-attachments/assets/d0ef0ef5-5b9d-4ad7-b21e-19049ae32ecc" />

<img width="1366" height="729" alt="Image" src="https://github.com/user-attachments/assets/be5a3805-58fc-4769-9be7-5a9a22061a90" />

<img width="1366" height="722" alt="Image" src="https://github.com/user-attachments/assets/6c997d6b-2f00-4469-9fd6-153dfa4f0540" />

<img width="1366" height="730" alt="Image" src="https://github.com/user-attachments/assets/c0c0b547-f779-4d02-98f6-0b7fc969ee62" />


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


