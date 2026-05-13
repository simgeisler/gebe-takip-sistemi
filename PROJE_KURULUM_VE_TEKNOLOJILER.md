# Proje kurulumu ve teknoloji özeti

Bu dosya, projeyi **ilk kez çalıştıracak biri** için hazırlanmıştır: hangi yazılımların kurulu olması gerektiği, sırayla ne yapılacağı, **frontend’in ne işe yaradığı** ve **backend / veritabanında hangi araçların** kullanıldığı burada özetlenir. Kısa teknik referans için kökteki `README.md` dosyasına da bakabilirsiniz.

---

## 1. Bu proje ne yapıyor?

**Bebeğim — Gebelik Takip**, hamilelik sürecinde kullanıcıya yardımcı olmayı hedefleyen bir web uygulamasıdır:

- Giriş ve kayıt
- Özet panel (dashboard), sağlık ölçümleri ve grafikler
- Takvim etkinlikleri
- Makale kütüphanesi
- Forum (sorular, yanıtlar, beğeniler)
- “Bebeğimle konuş” sohbet ekranı
- PDF rapor gibi API uçları

**Veri** sunucuda tutulur: tarayıcıdaki arayüz (frontend), HTTP ile FastAPI sunucusuna (backend) bağlanır; backend **PostgreSQL**e yazar/okur. Bu projede veritabanı pratikte **[Supabase](https://supabase.com)** üzerinde barındırılan PostgreSQL ile kullanılır (`DATABASE_URL`). Yerel bir Postgres sunucusu da aynı şekilde kullanılabilir.

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
```

- Gerçek host, port, kullanıcı ve şifreyi **kendi Supabase panelinizdeki** “Connection string” alanından kopyalayın; yukarıdaki satır sadece biçim örneğidir.
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
| **pytest** + **httpx** | API testleri |
| **Supabase** (altyapı) | Barındırılan **PostgreSQL**; ekstra bir `supabase` Python paketi yok, yalnızca Postgres URI’si (`DATABASE_URL`) |

Uygulama girişi: kök `backend/main.py` → `app.main` içindeki FastAPI örneği; yönlendirmeler `backend/app/routers/` altında modüllere ayrılmıştır.

---

## 9. Veritabanı katmanı ve Supabase’in yeri

- **Tek kalıcı veri deposu:** **PostgreSQL**. Projede bu genelde **Supabase** projesindeki Postgres örneğidir; bağlantı `DATABASE_URL` ile verilir.
- **ORM:** SQLAlchemy (`backend/app/models/`, `backend/app/core/database.py`).
- **Şema değişiklikleri:** Alembic migrasyonları (`alembic upgrade head`).

**Frontend ↔ Supabase:** Arayüz doğrudan Supabase’e bağlanmaz; `@supabase/supabase-js` kullanılmaz. Tarayıcı yalnızca **kendi FastAPI backend’inize** istek atar; veritabanı erişimi yalnızca backend sürecinde olur. Bu sayede RLS veya Supabase Dashboard ile yine aynı Postgres üzerinde yönetim yapabilirsiniz; uygulama kodu tarafında “bulut veritabanı = Supabase Postgres URI” modelidir.

**Ayrı bir “frontend içi veritabanı” yoktur**; geliştirmede veri her zaman **backend → PostgreSQL (Supabase veya yerel)** hattındadır.

---

## 10. Sorun giderme (kısa)

| Durum | Kontrol |
|--------|---------|
| Backend açılmıyor / DB hatası | `.env` içinde `DATABASE_URL` doğru mu; Supabase’te proje uyku modundan uyandı mı; yerel Postgres ise servis çalışıyor mu; `alembic upgrade head` çalıştı mı? |
| Frontend API’ye ulaşamıyor | Backend 8000’de mi; `VITE_API_URL` doğru mu; tarayıcı konsolunda CORS veya ağ hatası |
| CORS hatası | Backend `app/main.py` içinde `CORSMiddleware` izin verilen origin listesi; geliştirme adresiniz (ör. `http://localhost:8080`) listede veya regex ile kapsanıyor mu? |

---

Bu dosya proje kökünde durur; güncelleme yaptıkça özellikle **port**, **ortam değişkeni adları** ve **yeni bağımlılıklar** bölümlerini senkron tutmanız iyi olur.
