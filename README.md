# 🤰 Bebeğim — Gebelik Takip

Modern, AI destekli gebelik takip ve sağlık yönetim platformu. Anne adaylarının gebelik sürecini baştan sona tek bir platform üzerinden, güvenle ve sağlıkla takip edebilmesi için geliştirilmiştir.

🔗 **Canlı Demo:** [gebe-takip-sistemi.vercel.app](https://gebe-takip-sistemi.vercel.app)

---

## 🌸 Genel Amaç

Gebe Takip Sistemi; dinamik sağlık veri analizleri, **kullanıcı verileriyle tam entegre çalışan yapay zekâ destekli asistanı** ve topluluk odaklı forum yapısıyla anne adaylarının hamilelik yolculuğundaki en büyük dijital destekçisidir.

### 🧭 Ana Modüller
* 📊 **Dashboard:** Sürecin genel ve anlık özeti.
* 🩺 **Sağlık Takibi:** Ölçüm kayıtları, grafiksel trendler ve PDF raporlama.
* 📅 **Takvim:** Randevu, ilaç ve etkinlik yönetimi.
* 📚 **Kütüphane:** Kategori bazlı uzman ve rehber içerikler.
* 💬 **Forum:** Anne adayları arası topluluk ve deneyim paylaşımı.
* 🤖 **Gebelik Asistanı (AI Chat):** Kişiselleştirilmiş, veriye dayalı akıllı asistan.

---

## 🚀 Modül Detayları

### 🏠 Dashboard (Özet Ekranı)
Dashboard ekranı, kullanıcının gebelik sürecine dair en kritik verileri tek bir bakışta sunar:
* **Kullanıcı Karşılama:** İsme özel dinamik karşılama.
* **Gebelik Bilgisi:** Kavuşmaya kalan gün sayısı, gebelik haftası (Ör: 6. hafta / 40) ve ilerleme yüzdesi.
* **Bebek Durumu:** Mevcut haftaya ait tahmini ağırlık, boy ve gelişim açıklamaları.
* **Sağlık Özeti:** Son girilen tansiyon, kan şekeri ve kilo takibi grafiği.
* **Takvim Özeti:** Yaklaşan etkinlikler ve hatırlatıcılar.
* **AI Hızlı Erişim:** Yapay zekâ asistanına hızlı geçiş alanı.

### 🩺 Sağlık Takibi & Raporlama
Kullanıcıların vital ve fiziksel sağlık verilerini kayıt altında tuttuğu modüldür.
* **Girilen Veriler:** Kilo, su tüketimi, tansiyon (sistolik / diastolik), kan şekeri, nabız ve kişisel notlar.
* **Özellikler:** Son kayıtların listelenmesi, grafiksel trend gösterimi ve kolay yeni ölçüm ekleme.
* **📄 PDF Rapor Oluşturma:** Kullanıcı, seçtiği başlangıç ve bitiş tarihlerine göre (veya tüm süreci kapsayacak şekilde) sağlık verilerini filtreleyip doktoruna sunmak üzere PDF formatında indirebilir.

### 📅 Takvim & Etkinlik Yönetimi
Randevu, ilaç ve etkinliklerin organize edildiği dinamik alan.
* **Yeni Etkinlik Ekleme:** Tarih, başlık, saat, konum (isteğe bağlı) ve kategori seçimi.
    * *Kategoriler:* İlaç, Randevu, Etkinlik
* **Görünüm:** Aylık takvim ekranı ve tüm etkinliklerin kronolojik listesi.

### 📚 Kütüphane (Bilgi Merkezi)
Hamilelik sürecine yönelik rehber yazıların ve uzman makalelerinin yer aldığı bölümdür.
* **Özellikler:** Kelime bazlı konu arama, kategori filtreleme.
* **İçerik Detayı:** Her içerikte başlık, açıklama, okuma süresi, beğeni sayısı ve kategori etiketi bulunur.

### 💬 Forum (Topluluk)
Anne adaylarının deneyim ve soru paylaştığı, birbirlerine destek olduğu sosyal alan.
* **Kategoriler:** Trimester 1-2-3, Beslenme & Takviyeler, Sağlık & Şikayetler, Bebek Alışverişi, Doğum Hazırlığı, Ruh Sağlığı, İsim Önerileri, Diğer.
* **Özellikler:** Yeni başlık açma, başlıklar altında yanıt sistemi, beğeni mekanizması, kullanıcı ve zaman damgası bilgisi.

### 🤖 Gebelik Asistanı (AI Chat) 
Sıradan sohbet botlarının aksine, platformun yapay zekâ asistanı **kullanıcının profil ve sağlık verilerine doğrudan erişim yeteneğine** sahiptir. Sistem, kullanıcıyı tanır ve tamamen kişiselleştirilmiş bir deneyim sunar:
* **Veri Duyarlı Analiz:** Kullanıcının sisteme kaydettiği anlık ve geçmiş sağlık verilerini (Tansiyon, Kan Şekeri, Kilo, Nabız) okuyabilir ve analiz edebilir.
* **Kişiselleştirilmiş Yorumlama:** "Bugünkü tansiyon değerim nasıl?" veya "Şeker ölçümlerimde bir anormallik var mı?" gibi sorulara, kullanıcının veri tabanındaki güncel kayıtlarını inceleyerek tıbbi referanslar dahilinde akıllı yorumlar sunar.
* **Haftaya Özel Dinamik Bilgilendirme:** Kullanıcının Son Adet Tarihi (SAT) üzerinden hesaplanan güncel gebelik haftasını (Ör: 12. hafta) otomatik olarak bilir. Gelişim tavsiyelerini, semptom yorumlarını ve beslenme önerilerini tamamen o haftaya özel olarak şekillendirir.
* **Proaktif Uyarı Mekanizması:** Sağlık verilerinde normal dışı bir trend (örneğin ardışık yüksek tansiyon) sezdiğinde kullanıcıyı doktoruna danışması yönünde rehberlik eder.
---

## 👥 Kullanıcı ve Sistem Yönetimi

### 👤 Giriş & Kayıt Sistemi
* **Giriş:** E-posta, Şifre ve Şifremi Unuttum akışı.
* **Kayıt:** Ad Soyad, E-posta, Şifre, **Son Adet Tarihi (SAT)** ve Başlangıç Kilo Bilgisi *(Gebelik hesaplamaları ve AI bağlamı bu verilere göre dinamik oluşturulur)*.

### 🌙 Profil & Arayüz
* Kullanıcı bilgilerini düzenleme.
* **Karanlık / Açık Mod (Dark/Light Mode)** geçiş desteği.
* Güvenli çıkış yapma seçeneği.

### 🔔 Bildirim Sistemi
* Forum etkileşimleri (Açılan başlığa gelen cevaplar, beğeniler vb.) için sistem içi anlık bildirimler.
* Okundu olarak işaretleme ve dinamik bildirim sayacı.
Full-stack gebelik takip uygulaması: sağlık takibi, takvim, forum, makaleler ve **AI destekli Gebelik Asistanı**.

## 📁 Proje Dosya Yapısı

/frontend   → Arayüz kodu (React + Vite) – mobil (iOS / Android) için genişletilebilir  
/backend    → API ve iş mantığı (FastAPI)  
/prodocs    → Yapay zekâ ajanları için geliştirme referans dosyaları  

.gitignore   → Gereksiz dosyaların repoya girmesini engeller  
README.md    → Uygulamanın amacı ve kurulum bilgileri  
.env.example → Örnek environment değişkenleri (API anahtarları olmadan)  

PRD.md          → Projenin amacı, problem tanımı ve temel özellikler  
tech-stack.md   → Kullanılan teknolojiler ve AI kullanım açıklamaları  
Plan.md         → Geliştirme adımları ve kullanıcı hikayeleri  
DesignSystem.md → UI tasarım kuralları (renk, font, component yapısı)  
Progress.md     → Geliştirme süreci ve yapılan işler  

## Tech Stack

- **Frontend:** React + Vite 
- **Backend:** FastAPI
- **Database:** PostgreSQL (Supabase)
- **ORM:** SQLAlchemy + Alembic
- **AI:** OpenRouter (LLM API)

## Ortam Değişkenleri (.env)

### Backend (`backend/.env`)

    DATABASE_URL=postgresql://postgres.[REF]:[PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
    OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
    OPENROUTER_MODEL=openai/gpt-oss-120b:free
    OPENROUTER_HTTP_REFERER=http://localhost:8080
    OPENROUTER_APP_TITLE=GebelikAsistani

### Frontend (`frontend/.env`)

    VITE_API_URL=http://localhost:8000/api/v1

---

## Hızlı Başlangıç

### Backend

    cd backend
    python -m venv .venv

    # Windows:
    .venv\Scripts\activate

    # Mac/Linux:
    source .venv/bin/activate

    pip install -r requirements.txt
    alembic upgrade head
    uvicorn main:app --reload --port 8000

---

### Frontend

    cd frontend
    npm install
    npm run dev
    
## Veritabanı Mimarisi

* **Veritabanı:** PostgreSQL (Supabase Cloud)
* **ORM:** SQLAlchemy
* **Migrasyon:** Alembic (`alembic upgrade head`)

---

## OpenRouter ile AI Entegrasyonu (Gebelik Asistanı)

**Sohbet Akışı:** `Frontend (BabyChat.tsx)` ➔ `FastAPI Backend (Veri & Bağlam Ekleme)` ➔ `OpenRouter API` ➔ `PostgreSQL (Kayıt)` ➔ `Frontend (Yanıt)`

### Model ve Ortam Değişkenleri (`backend/.env`)

* **Kullanılan Model:** `openai/gpt-oss-120b:free`

###  API Anahtarı Nasıl Alınır?
1. [openrouter.ai](https://openrouter.ai/) sitesinde hesap açın.
2. **API Keys** bölümünden yeni bir anahtar üretin.
3. Bu anahtarı `backend/.env` içindeki `OPENROUTER_API_KEY` alanına yapıştırıp backend'i (`uvicorn`) yeniden başlatın.

## 🚀 Geliştirme Vizyonu (Roadmap)

Future-proof bir yapıyla uygulamanın gelecekte kazanması planlanan özellikler:
- [ ] **Mobil Uygulama:** iOS ve Android (React Native / Flutter) sürümlerinin geliştirilmesi.
- [ ] **Gelişmiş AI Analiz Sistemi:** Trend analizlerine dayalı erken uyarı ve anomali tespiti.
- [ ] **Doktor Paneli:** Anne adayının onay verdiği doktorun verileri canlı takip edebileceği web arayüzü.
- [ ] **Akıllı Bildirimler:** Su içme, ilaç saati ve randevular için anlık push bildirimleri.
- [ ] **Çoklu Dil Desteği:** Global kullanıcı kitlesi için entegrasyon.

