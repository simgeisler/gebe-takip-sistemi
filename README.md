# Bebeğim — Gebelik Takip

Vite + React + TypeScript arayüzü ve FastAPI tabanlı API ile gebelik takibi: ölçümler, takvim, forum, kütüphane, sohbet ve PDF rapor uçları birlikte çalışır. API yolları `frontend/src` içindeki sayfalar ve `frontend/src/lib/api.ts` ile uyumludur.

## Gereksinimler

- **Node.js** (LTS önerilir)
- **Python 3.12** (bkz. `backend/.python-version`)
- **PostgreSQL** — backend `DATABASE_URL` ile bağlanır (projede pratikte **[Supabase](https://supabase.com)** üzerindeki Postgres; yerel Postgres de olur)

## Klasör yapısı

| Klasör | Açıklama |
|--------|----------|
| `frontend` | Web uygulaması (Vite, Tailwind, shadcn tarzı bileşenler) |
| `backend` | FastAPI uygulaması, SQLAlchemy, Alembic |

## Ortam değişkenleri

**Backend** — `backend` içinde `.env` oluşturun:

```env
# Yerel örnek:
DATABASE_URL=postgresql://KULLANICI:SIFRE@localhost:5432/VERITABANI_ADI
# Supabase: Project Settings → Database → Connection string (URI) değerini kullanın.
```

`python-dotenv` bu dosyayı yükler; `DATABASE_URL` yoksa veritabanı oturumu açılmaz.

**Frontend** (isteğe bağlı) — `frontend/.env` veya `.env.local`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Belirtilmezse `api.ts` içindeki varsayılan (`http://localhost:8000/api/v1`) kullanılır.

## Veritabanı ve migrasyonlar

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

## Geliştirme (Windows)

İki ayrı terminal kullanın: önce API, sonra arayüz.

### Backend

```powershell
cd backend
.\.venv\Scripts\activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Sağlık: [http://127.0.0.1:8000/healthz](http://127.0.0.1:8000/healthz) — `api` alanında kök önek: **`/api/v1`**

Reload ile sorun yaşarsanız `--reload` kaldırın veya `--reload --reload-dir app` deneyin.

### Frontend

`frontend/vite.config.ts` geliştirme sunucusunu **8080** portuna ayarlar:

```powershell
cd frontend
npm install
npm run dev
```

Tarayıcı: [http://localhost:8080](http://localhost:8080) (veya [http://127.0.0.1:8080](http://127.0.0.1:8080))

Üretim derlemesi: `npm run build` → çıktı `frontend/dist`

### CORS

Backend, `localhost` / `127.0.0.1` / `[::1]` üzerinde yaygın portları (5173, 4173, 8080, 8081, 19006 vb.) ve bu adresler için regex ile CORS’a izin verir. Farklı bir host/port kullanıyorsanız `backend/app/main.py` içindeki `CORSMiddleware` listesini güncellemeniz gerekir.

## Testler

```powershell
# Backend
cd backend
.\.venv\Scripts\activate
pytest tests

# Frontend (proje kökünden)
cd frontend
npm run test
```

## API ↔ ekran özeti

Tüm yollar kökten **`/api/v1`** ile başlar. Çoğu kullanıcı verisi için `Authorization: Bearer <token>` gerekir.

| Ekran | Kaynak (sayfa) | Örnek uçlar |
|--------|----------------|-------------|
| **Dashboard** | `Dashboard.tsx` | `GET /dashboard` — özet, grafikler, yaklaşanlar (JWT) |
| **Sağlık takibi** | `HealthTracking.tsx` | `GET/POST/PUT/DELETE /measurements`, `GET /measurements/charts` (JWT); ek özet/trend: `GET /health/measurements/summary`, `GET /health/measurements/trends` … (JWT) |
| **Takvim** | `CalendarPage.tsx` | `GET/POST/PUT/DELETE /calendar/events` (JWT) |
| **Yaklaşanlar** | Dashboard `upcoming` | `GET/POST/PUT/DELETE /upcoming/` (JWT) |
| **Kütüphane** | `Library.tsx`, `LibraryArticle.tsx` | `GET/POST /library/articles`, `GET/PUT/DELETE /library/articles/{id}` (liste ve detay JWT) |
| **Forum** | `Forum.tsx`, `ForumQuestion.tsx` | `GET /forum`, `POST /forum`, `GET/PUT/DELETE /forum/questions/{id}`, yanıtlar ve beğeniler (liste genelde herkese açık; yazma JWT) — ayrıca eski kart API’si: `GET /forum/threads` … |
| **Bebeğimle konuş** | `BabyChat.tsx` | `GET/POST/PUT/DELETE /chat/messages` — gövde `{ "from": "baby"\|"me", "text": "..." }` (JWT) |
| **Giriş / kayıt** | `Login.tsx`, `SignUp.tsx` | `POST /auth/register`, `POST /auth/login`, `GET/PATCH /auth/me` |
| **PDF rapor** | — | `GET /reports/pdf` (JWT) |
| Tekme / kasılma | — | `GET/POST/... /wellbeing/kick-sessions`, `POST /wellbeing/contractions/analyze` (JWT) |

`backend/app/routers/content_router.py` içinde haftalık içerik ve kütüphane CRUD tanımları bulunur; bu router şu an `app/main.py` içinde **kayıtlı değil**. Haftalık içerik uçlarını kullanacaksanız router’ı uygulamaya eklemeniz gerekir.
