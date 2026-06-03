# Bebeğim — Gebelik Takip
---

## 1. Bu proje ne yapıyor?

**Bebeğim — Gebelik Takip**, hamilelik sürecinde kullanıcıya yardımcı olmayı hedefleyen bir web uygulamasıdır:

- Giriş ve kayıt
- Özet panel (dashboard), sağlık ölçümleri ve grafikler
- Takvim etkinlikleri
- Makale kütüphanesi
- Forum (sorular, yanıtlar, beğeniler)
- “Gebelik Asistan” sohbet ekranı (OpenRouter üzerinden AI destekli)
- PDF rapor gibi API uçları

**Veri** sunucuda tutulur: tarayıcıdaki arayüz (frontend), HTTP ile FastAPI sunucusuna (backend) bağlanır; backend **PostgreSQL**e yazar/okur. Bu projede veritabanı pratikte **[Supabase](https://supabase.com)** üzerinde barındırılan PostgreSQL ile kullanılır (`DATABASE_URL`). Yerel bir Postgres sunucusu da aynı şekilde kullanılabilir.

 ## Ekran Görüntüleri
<img width="1919" height="1031" alt="Image" src="https://github.com/user-attachments/assets/6e9888c6-b050-4931-82a3-b286184428a3" />

<img width="1919" height="1029" alt="Image" src="https://github.com/user-attachments/assets/6590575f-cd99-45e7-8de3-22c788933204" />

<img width="1919" height="1028" alt="Image" src="https://github.com/user-attachments/assets/c1fb8e94-b897-4fce-a43a-0a7286f71795" />

<img width="1919" height="1023" alt="Image" src="https://github.com/user-attachments/assets/83b01a79-9f93-4f4c-a953-06f0d1486374" />

<img width="1916" height="1022" alt="Image" src="https://github.com/user-attachments/assets/951d0baf-6e71-4a8b-9979-b67f9ceafbe1" />

<img width="1919" height="1018" alt="Image" src="https://github.com/user-attachments/assets/2cd653db-9d3e-4a08-a3ed-a3db95bda873" />

<img width="1919" height="1032" alt="Image" src="https://github.com/user-attachments/assets/891a2997-ac8e-4253-b482-05f33793aae3" />

<img width="1919" height="1020" alt="Image" src="https://github.com/user-attachments/assets/eae5cbd8-b96b-4966-ade0-a9590e9be68e" />

<img width="1917" height="1035" alt="Image" src="https://github.com/user-attachments/assets/b3d41f62-56a3-49ff-b650-d476a2bebbbc" />

<img width="1919" height="1030" alt="Image" src="https://github.com/user-attachments/assets/902d245c-e341-498d-9bff-443d16665c32" />

<img width="1919" height="1025" alt="Image" src="https://github.com/user-attachments/assets/80bc3c42-1102-4fc2-955b-fd09b5b272b0" />

<img width="1919" height="1016" alt="Image" src="https://github.com/user-attachments/assets/1b66b062-befa-43eb-8bdf-e665846b63f3" />

<img width="1919" height="1032" alt="Image" src="https://github.com/user-attachments/assets/ad05c5f1-9bef-45b4-a3a0-43d11290a20a" />


---

## 2. Kurulumdan önce bilgisayarınızda olması gerekenler

| Yazılım | Not |
|--------|-----|
| **Node.js** | LTS sürümü yeterli; `npm` ile paket kurulumu |
| **Python 3.12** | Projede `backend/.python-version` ile 3.12 işaretli |
| **PostgreSQL erişimi** | **[Supabase](https://supabase.com)** projesi (önerilen) veya kendi kurduğunuz Postgres; bağlantı dizesi `backend/.env` içindeki `DATABASE_URL` |
| **Git** (isteğe bağlı) | Repoyu klonlamak için |

Windows’ta PowerShell veya CMD kullanabilirsiniz. macOS / Linux’ta komutlar benzer; sanal ortam aktivasyonu `source .venv/bin/activate` şeklindedir.

---

## 3. Veritabanı hazırlığı (Supabase veya yerel Postgres)

### Supabase ile (bu projedeki kullanım)

Uygulama **Supabase Auth veya Supabase JavaScript istemcisini** doğrudan kullanmaz; Supabase’i **yönetilen PostgreSQL** olarak kullanırsınız. Bağlantı standart `postgresql://...` URI’si ile **SQLAlchemy + psycopg2** üzerinden yapılır (`backend/app/core/database.py`). Kodda da bu yaklaşım not düşülür (`backend/app/services/store.py`).

1. [Supabase](https://supabase.com) üzerinde proje oluşturun.
2. **Project Settings → Database** bölümünden bağlantı bilgisini alın:
   - **Connection string** (URI), genelde **Session mode** havuzlayıcı (pooler) veya **Direct connection** adresi olarak verilir.
3. `backend` klasöründe `.env` oluşturun veya güncelleyin:

```env
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-oss-120b:free
```

- Gerçek host, port, kullanıcı ve şifreyi **kendi Supabase panelinizdeki** “Connection string” alanından kopyalayın; yukarıdaki satır sadece biçim örneğidir.
- `OPENROUTER_API_KEY` sohbet asistanı için zorunludur; anahtar [openrouter.ai](https://openrouter.ai/) hesabından alınır (aşağıdaki **10. bölüm**).
- **Şifreleri repoya eklemeyin**; `.env` dosyası `.gitignore` içinde kalmalıdır. `alembic upgrade head` çalıştırırken `DATABASE_URL` ortam değişkeni yeterlidir (`alembic/env.py` bunu okuyup `sqlalchemy.url` olarak ayarlar).

### Yerel PostgreSQL

Kendi makinenizde Postgres kullanacaksanız veritabanı oluşturup benzer şekilde:

```env
DATABASE_URL=postgresql://KULLANICI_ADI:SIFRE@localhost:5432/VERITABANI_ADI
```

---

## 4. Backend’i çalıştırma

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

- API dokümantasyonu: **http://127.0.0.1:8000/docs**
- Sağlık kontrolü: **http://127.0.0.1:8000/healthz**
- Tüm iş API’leri kök önek ile: **`/api/v1/...`**

`DATABASE_URL` yanlış veya eksikse uygulama veritabanı oturumu açamaz; önce `.env` ve migrasyonları doğrulayın.

---

## 5. Frontend’i çalıştırma

```powershell
cd frontend
npm install
npm run dev
```

Varsayılan geliştirme adresi bu projede **http://localhost:8080** (ayar `frontend/vite.config.ts` içinde `port: 8080`).

Backend farklı bir makinede veya porttaysa, `frontend` içinde `.env` veya `.env.local` oluşturup şunu ekleyin:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Kodda varsayılan taban adres `frontend/src/lib/api.ts` içinde tanımlıdır; ortam değişkeni bunun üzerine yazar.

**Özet:** Önce backend (8000), sonra frontend (8080) açık olsun; tarayıcıdan 8080’e gidin, giriş/kayıt ve korumalı sayfalar API’ye istek atar.

---

## 6. Frontend: ne rol oynuyor, nerede ne var?

Frontend **sadece kullanıcı arayüzü ve istemci tarafı mantığıdır**; kalıcı veri burada tutulmaz (oturum için tarayıcıda `localStorage` ile erişim jetonu saklanabilir).

| Bölüm | Rol |
|--------|-----|
| `frontend/src/pages/` | Tam sayfa ekranlar: giriş, kayıt, dashboard, sağlık, takvim, kütüphane, forum, sohbet vb. |
| `frontend/src/components/` | Yeniden kullanılan arayüz parçaları; `components/ui/` altında Radix tabanlı bileşenler (buton, kart, diyalog …) |
| `frontend/src/lib/api.ts` | Backend’e giden `fetch` çağrılarının merkezi istemcisi; yol ve JWT başlığı burada toplanır |
| `frontend/src/App.tsx` | Rotalar (`react-router-dom`): `/dashboard`, `/saglik`, `/takvim`, `/kutuphane`, `/forum`, `/bebegimle-konus` vb. |
| `frontend/index.html` + `src/main.tsx` | Uygulamanın giriş noktası |

Kullanıcı bir form doldurduğunda veya liste yüklediğinde, React sayfaları `api.ts` üzerinden FastAPI’ye JSON isteği gönderir; gelen cevaba göre ekran güncellenir.


---

## 7. Frontend’de kullanılan başlıca araçlar ve kütüphaneler

| Araç / kütüphane | Ne için kullanılıyor? |
|------------------|------------------------|
| **React 18** | Bileşen tabanlı arayüz |
| **TypeScript** | Tip güvenliği |
| **Vite** | Geliştirme sunucusu ve üretim derlemesi (hızlı HMR) |
| **@vitejs/plugin-react-swc** | React derlemesi için SWC |
| **React Router v6** | Sayfa yolları ve yönlendirme |
| **TanStack React Query v5** | Sunucu verisi için önbellekleme, yeniden istek, yükleme durumları (`App.tsx` içinde `QueryClientProvider`) |
| **Tailwind CSS** | Yardımcı sınıflarla stil |
| **Radix UI** (`@radix-ui/react-*`) | Erişilebilir, stilsiz primitive bileşenler (diyalog, menü, sekme …) |
| **react-hook-form** + **zod** + **@hookform/resolvers** | Formlar ve şema ile doğrulama |
| **Recharts** | Grafikler (ör. sağlık / dashboard) |
| **date-fns** | Tarih işlemleri |
| **lucide-react** | İkonlar |
| **sonner** / shadcn tarzı **toast** | Bildirimler |
| **Vitest** + **Testing Library** | Birim / bileşen testleri (`npm run test`) |
| **ESLint** | Kod kalitesi (`npm run lint`) |

Özet: **Vite + React + TypeScript** iskeleti; **Tailwind + Radix** ile modern UI; **React Query** ile API verisi; formlarda **react-hook-form + zod**.

---

## 8. Backend’de kullanılan başlıca araçlar

| Araç / kütüphane | Ne için kullanılıyor? |
|------------------|------------------------|
| **FastAPI** | HTTP API, otomatik OpenAPI (`/docs`) |
| **Uvicorn** | ASGI sunucusu (uygulamayı çalıştırma) |
| **Pydantic** | İstek/yanıt modelleri ve doğrulama |
| **SQLAlchemy** | ORM: tablolar ve sorgular Python nesneleriyle |
| **Alembic** | Veritabanı şema migrasyonları (`alembic/` klasörü) |
| **psycopg2-binary** | PostgreSQL sürücüsü (Supabase veya yerel Postgres’e bağlanır) |
| **python-jose** | JWT işlemleri |
| **passlib** + **bcrypt** | Parola özetleme |
| **python-dotenv** | `.env` dosyasından `DATABASE_URL` vb. okuma |
| **httpx** | OpenRouter’a `POST /api/v1/chat/completions` istekleri (`openrouter_client.py`) |
| **pytest** + **httpx** | API testleri |
| **OpenRouter** | LLM sağlayıcısı; varsayılan model **OpenAI: gpt-oss-120b (free)** → `openai/gpt-oss-120b:free` |
| **Supabase** (altyapı) | Barındırılan **PostgreSQL**; ekstra bir `supabase` Python paketi yok, yalnızca Postgres URI’si (`DATABASE_URL`) |

Uygulama girişi: kök `backend/main.py` → `app.main` içindeki FastAPI örneği; yönlendirmeler `backend/app/routers/` altında modüllere ayrılmıştır.

---
- **Tek kalıcı veri deposu:** **PostgreSQL**. Projede bu genelde **Supabase** projesindeki Postgres örneğidir; bağlantı `DATABASE_URL` ile verilir.
- **ORM:** SQLAlchemy (`backend/app/models/`, `backend/app/core/database.py`).
- **Şema değişiklikleri:** Alembic migrasyonları (`alembic upgrade head`).

**Frontend ↔ Supabase:** Arayüz doğrudan Supabase’e bağlanmaz; `@supabase/supabase-js` kullanılmaz. Tarayıcı yalnızca **kendi FastAPI backend’inize** istek atar; veritabanı erişimi yalnızca backend sürecinde olur. Bu sayede RLS veya Supabase Dashboard ile yine aynı Postgres üzerinde yönetim yapabilirsiniz; uygulama kodu tarafında “bulut veritabanı = Supabase Postgres URI” modelidir.

**Ayrı bir “frontend içi veritabanı” yoktur**; geliştirmede veri her zaman **backend → PostgreSQL (Supabase veya yerel)** hattındadır.

---
## 9. Veritabanı katmanı ve Supabase’in yeri

- **Tek kalıcı veri deposu:** **PostgreSQL**. Projede bu genelde **Supabase** projesindeki Postgres örneğidir; bağlantı `DATABASE_URL` ile verilir.
- **ORM:** SQLAlchemy (`backend/app/models/`, `backend/app/core/database.py`).
- **Şema değişiklikleri:** Alembic migrasyonları (`alembic upgrade head`).

**Frontend ↔ Supabase:** Arayüz doğrudan Supabase’e bağlanmaz; `@supabase/supabase-js` kullanılmaz. Tarayıcı yalnızca **kendi FastAPI backend’inize** istek atar; veritabanı erişimi yalnızca backend sürecinde olur. Bu sayede RLS veya Supabase Dashboard ile yine aynı Postgres üzerinde yönetim yapabilirsiniz; uygulama kodu tarafında “bulut veritabanı = Supabase Postgres URI” modelidir.

**Ayrı bir “frontend içi veritabanı” yoktur**; geliştirmede veri her zaman **backend → PostgreSQL (Supabase veya yerel)** hattındadır.

---

## 10. OpenRouter ile AI entegrasyonu (Gebelik Asistanı)

**Bebeğimle konuş** ekranındaki yanıtlar, tarayıcıdan doğrudan bir modele gitmez. Frontend `POST /api/v1/chat/assistant` çağırır; backend bağlamı hazırlayıp **[OpenRouter](https://openrouter.ai/)** üzerinden LLM’e iletir ve yanıtı PostgreSQL’deki sohbet tablolarına kaydeder.

### Kullanılan model

| OpenRouter panelinde görünen ad | Ortam değişkeni / API `model` değeri |
|--------------------------------|--------------------------------------|
| **OpenAI: gpt-oss-120b (free)** | `openai/gpt-oss-120b:free` |

Bu, OpenRouter’daki ücretsiz katmanlı **gpt-oss-120b** modelidir. `OPENROUTER_MODEL` tanımlı değilse backend aynı değeri varsayılan olarak kullanır (`backend/app/services/openrouter_client.py`).

### Ortam değişkenleri (`backend/.env`)

| Değişken | Zorunlu | Açıklama | Varsayılan |
|----------|---------|----------|------------|
| `OPENROUTER_API_KEY` | Evet | OpenRouter API anahtarı (`sk-or-v1-...`) | — |
| `OPENROUTER_MODEL` | Hayır | Model kimliği | `openai/gpt-oss-120b:free` |
| `OPENROUTER_HTTP_REFERER` | Hayır | OpenRouter `HTTP-Referer` başlığı | `http://localhost:5173` |
| `OPENROUTER_APP_TITLE` | Hayır | OpenRouter `X-Title` başlığı (ASCII) | `Gebelik Asistani` |

Örnek `backend/.env` satırları için `backend/.env.example` dosyasına bakın. API anahtarını repoya eklemeyin.

### Anahtar alma

1. [openrouter.ai](https://openrouter.ai/) üzerinde hesap açın.
2. **API Keys** bölümünden yeni anahtar oluşturun.
3. Anahtarı `backend/.env` içindeki `OPENROUTER_API_KEY` alanına yapıştırın.
4. Backend’i yeniden başlatın (`uvicorn` süreci `.env` değişikliklerini yeniden yükler).

### Kodda akış (özet)

```
BabyChat.tsx  →  POST /api/v1/chat/assistant
       →  chat_service.py  →  assistant_service.py (sistem promptu + bağlam)
       →  openrouter_client.chat_completion()
       →  https://openrouter.ai/api/v1/chat/completions
       →  yanıt chat_messages tablosuna yazılır
```

| Katman | Dosya |
|--------|-------|
| OpenRouter istemcisi | `backend/app/services/openrouter_client.py` |
| Prompt ve bağlam | `backend/app/services/assistant_service.py` |
| Sohbet CRUD + orchestration | `backend/app/services/chat_service.py` |
| HTTP uçları | `backend/app/routers/chat_router.py` |
| Arayüz | `frontend/src/pages/BabyChat.tsx` |

İstemci `httpx` ile OpenRouter’a istek atar; istek gövdesinde `reasoning: { enabled: true, exclude: true }` kullanılır (iç düşünme ayrı alanda kalır, sohbet metni `content` üzerinden okunur). Zaman aşımı yaklaşık **90 saniye**dir.

### Hata kodları (kullanıcıya yansıyan)

| Durum | HTTP |
|--------|------|
| `OPENROUTER_API_KEY` yok / boş | 503 |
| OpenRouter veya ağ hatası | 502 |
| Yanıt süresi aşıldı | 504 |

### Ek dokümantasyon

Detaylı mimari ve güvenlik kuralları `prodocs/` altında: `openrouter-entegrasyonu.md`, `gebelik-asistani-mimari.md`, `chat-akisi.md`, `sistem-promptlari.md`.

---

## 11. Sorun giderme (kısa)

| Durum | Kontrol |
|--------|---------|
| Backend açılmıyor / DB hatası | `.env` içinde `DATABASE_URL` doğru mu; Supabase’te proje uyku modundan uyandı mı; yerel Postgres ise servis çalışıyor mu; `alembic upgrade head` çalıştı mı? |
| Frontend API’ye ulaşamıyor | Backend 8000’de mi; `VITE_API_URL` doğru mu; tarayıcı konsolunda CORS veya ağ hatası |
| CORS hatası | Backend `app/main.py` içinde `CORSMiddleware` izin verilen origin listesi; geliştirme adresiniz (ör. `http://localhost:8080`) listede veya regex ile kapsanıyor mu? |
| Sohbet “AI yapılandırılmamış” / 503 | `backend/.env` içinde `OPENROUTER_API_KEY` var mı; backend yeniden başlatıldı mı? |
| Sohbet 502 / boş yanıt | `OPENROUTER_MODEL` doğru mu (`openai/gpt-oss-120b:free`); OpenRouter’da ücretsiz model kotası dolmuş olabilir |

---




