# Gebelik Takibi MVP

Bu repo, PRD/MVP'e uygun olarak `Expo + FastAPI + PostgreSQL + Firebase Auth` tabanli MVP iskeleti icerir.

## Klasorler

- `backend/`: FastAPI API, veri modelleri ve endpoint'ler
- `frontend/`: Expo React Native uygulamasi

## Backend calistirma

1. Python sanal ortam olustur.
2. `pip install -r backend/requirements.txt`
3. `backend/.env.example` dosyasini baz alarak ortam degiskenlerini ayarla.
4. `uvicorn main:app --reload` komutunu `backend/` icinde calistir.

## Frontend calistirma

1. `cd frontend`
2. `npm install`
3. `.env.example` dosyasini `.env` olarak kopyala ve `EXPO_PUBLIC_API_BASE_URL` degerini backend adresine ayarla (lokalde varsayilan `http://localhost:8000`).
4. `src/shared/firebase/firebase.ts` icinde Firebase config degerlerini doldur.
5. `npm run start`

## MVP kapsaminda gelen temel ozellikler

- Firebase email/sifre auth ve backend token dogrulama
- Onboarding: SAT/EDD + baslangic kilosu
- Dashboard: hafta/gun/trimester/geri sayim + son kilo/tansiyon
- Kilo ve tansiyon log endpointleri + mobil arayuz
- Haftalik metadata endpointi (1-42 seed)
- Tekme / kasilma kaydi ve 5-1-1 analizi
- Kutuphane arama + forum (kategori/thread/reply/report)
- PDF export endpointi (stream)
- Bildirim token kaydi ve ornek haftalik push cron scripti
