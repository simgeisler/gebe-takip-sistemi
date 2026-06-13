# 📦 Tech Stack & Mimari Seçimler

**Proje:** Bebeğim – Gebelik Takip Uygulaması  
**Doküman:** `tech-stack.md`  
**Amaç:** Kullanılan teknolojileri, servis seçimlerini ve geliştirme yaklaşımını açıklamak  

---

## 1. 🧠 Genel Mimari Yaklaşım

Bu proje **full-stack web uygulaması** olarak tasarlanmıştır ve 3 katmandan oluşur:

- **Frontend (Client):** Kullanıcı arayüzü (React tabanlı)
- **Backend (API):** İş mantığı ve servis katmanı (FastAPI)
- **Database:** Kalıcı veri saklama (PostgreSQL – Supabase üzerinde yönetiliyor)

📌 **Veri akışı:**

Frontend (React) → HTTP (REST API) → Backend (FastAPI) → ORM (SQLAlchemy) → Database (PostgreSQL / Supabase)

---

## 2. 🎨 Frontend Teknolojileri

### 🔹 Kullanılan ana teknolojiler

- React 18  
- TypeScript  
- Vite  
- Tailwind CSS  
- React Router v6  
- TanStack React Query  
- Radix UI  
- react-hook-form + Zod  
- Recharts  
- Lucide Icons  

### 🔹 Seçim gerekçeleri

#### React + TypeScript
- Bileşen bazlı yapı ile ölçeklenebilir UI geliştirme  
- TypeScript ile hata azaltma ve güçlü tip güvenliği  

#### Vite
- Çok hızlı geliştirme sunucusu (HMR)  
- Modern build pipeline  

#### Tailwind CSS
- Component CSS yazmadan hızlı UI geliştirme  
- Mobil uyumluluk ve tutarlı tasarım sistemi  

#### React Query
- API verisini cache’leme  
- Loading/error state yönetimini otomatikleştirme  

#### Radix UI
- Hazır ama “unstyled” erişilebilir UI primitive’leri  
- Özelleştirilebilir modern component yapısı  

#### Zod + react-hook-form
- Form validasyonunu güçlü ve tip güvenli hale getirme  

---

## 3. ⚙️ Backend Teknolojileri

### 🔹 Kullanılan ana teknolojiler

- FastAPI  
- Uvicorn  
- SQLAlchemy  
- Alembic  
- Pydantic  
- PostgreSQL (Supabase)  
- psycopg2  
- python-jose (JWT)  
- passlib + bcrypt  
- httpx  
- python-dotenv  

### 🔹 Seçim gerekçeleri

#### 🚀 FastAPI
- Yüksek performanslı async API yapısı  
- Otomatik Swagger dokümantasyonu (`/docs`)  
- Pydantic ile güçlü veri doğrulama  

#### 🗄 PostgreSQL + Supabase
- Güvenilir ve ölçeklenebilir relational database  
- Supabase ile yönetilen cloud PostgreSQL altyapısı  
- Ek backend lock-in olmadan sadece DB hosting kullanımı  

#### 🧩 SQLAlchemy + Alembic
- ORM ile Python nesne–veri tabanı eşlemesi  
- Versiyonlanabilir database migration sistemi  

#### 🔐 JWT + bcrypt
- Güvenli kimlik doğrulama  
- Parola hashleme ve token bazlı authentication  

---

## 4. 🗄 Veritabanı Mimarisi

- Tek kaynak: PostgreSQL  
- Yönetim: Supabase  
- ORM: SQLAlchemy  
- Migration: Alembic  

📌 **Önemli tasarım kararı:**

Frontend asla doğrudan veritabanına bağlanmaz.  
Tüm veri akışı backend üzerinden gerçekleşir.

Bu yaklaşım:

- Güvenliği artırır  
- Yetkilendirmeyi merkezi hale getirir  
- API kontrolünü kolaylaştırır  

---

## 5. 🤖 AI Entegrasyonu (Gebelik Asistanı)

### 🔹 Kullanılan servis

- OpenRouter  

LLM erişimi OpenRouter üzerinden sağlanır.  
Varsayılan model: `openai/gpt-oss-120b:free`

### 🔹 Mimari akış

Frontend Chat UI → FastAPI /chat endpoint → Assistant Service (context + prompt) → OpenRouter API → Model response → PostgreSQL (chat log)

### 🔹 Neden OpenRouter?

- Tek API ile birden fazla model erişimi  
- Ücretsiz modellerle MVP maliyetsiz geliştirme  
- OpenAI uyumlu API formatı  

---

## 6. 🧪 Geliştirme Araçları ve Kalite

### Frontend

- ESLint → kod standardı  
- Vitest → test framework  
- React Testing Library → UI testleri  

### Backend

- pytest → API testleri  
- Pydantic → input validation  
- Uvicorn reload → hızlı geliştirme döngüsü  

---

## 7. 🧑‍💻 AI Kullanımı (Geliştirme Süreci)

Bu projede AI, sadece ürün içinde değil geliştirme sürecinin kendisinde de aktif olarak kullanılmıştır:

### 🔹 Kullanım alanları

#### 1. Kod üretimi ve refactor
- FastAPI endpoint tasarımı  
- React component yapıları  
- Form validation ve state management  

#### 2. Mimari karar destekleri
- PostgreSQL + Supabase mimarisi  
- Backend–frontend separation  
- Chat sistem tasarımı  

#### 3. Debugging
- CORS hataları  
- API entegrasyon sorunları  
- Environment variable problemleri  

#### 4. Dokümantasyon
- README  
- API açıklamaları  
- Teknik mimari dosyaları  

### 🔹 AI’nin rolü

- “Kod yazan araç” değil  
- “Mimari ve geliştirme asistanı”  
- Hızlı prototipleme ve karar doğrulama aracı  

---

## 8. 🧩 Servis Seçim Özeti

| Katman      | Teknoloji      | Neden |
|------------|---------------|------|
| Frontend   | React + Vite   | Hızlı, modern UI geliştirme |
| Styling    | Tailwind CSS   | Hızlı ve ölçeklenebilir tasarım |
| Backend    | FastAPI        | Performans + async yapı |
| DB         | PostgreSQL     | Güçlü relational yapı |
| DB Hosting | Supabase       | Yönetilen cloud DB |
| ORM        | SQLAlchemy     | Python veri modeli uyumu |
| Migration  | Alembic        | Versiyonlu DB değişiklikleri |
| AI         | OpenRouter     | Esnek LLM erişimi |

---

## 9. 📌 Sonuç

Bu teknoloji yığını şu hedefleri sağlar:

- ⚡ Hızlı geliştirme (Vite + FastAPI)  
- 🔐 Güvenli veri yönetimi (JWT + PostgreSQL)  
- 📈 Ölçeklenebilir mimari (API tabanlı yapı)  
- 🤖 AI destekli kullanıcı deneyimi (OpenRouter entegrasyonu)  