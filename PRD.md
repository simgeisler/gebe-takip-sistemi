# PRD: Bebeğim — Gebelik Takip (Web MVP)

**Ürün sloganı:** Haftalık veri, sağlık kaydı ve süreç yönetimi  
**Versiyon:** 2.0 (Web MVP — güncel)  
**Durum:** Aktif geliştirme — çekirdek özellikler canlı  
**Platform:** Web (Vite + React)

**Teknik referans:** [`PROJE_KURULUM_VE_TEKNOLOJILER.md`](PROJE_KURULUM_VE_TEKNOLOJILER.md)

---

## 1. Ürün özeti ve hedefler

**Bebeğim — Gebelik Takip**, hamile bireylere gebelik sürecini veri odaklı bir panel üzerinden takip etme imkânı sunan bir **web uygulamasıdır**. MVP başarısı; veri giriş hızı, dashboard doğruluğu, sağlık grafikleri, forum etkileşimi ve Danışma AI kalitesiyle ölçülür.

**Hedef kitle:** 20–36 yaş arası, gebelik sürecini dijital olarak izlemek isteyen kullanıcılar.

---

## 2. Teknoloji stack (güncel)

| Katman | Seçim |
|--------|--------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Radix UI, React Router v6, TanStack React Query |
| **Backend** | Python 3.12, FastAPI, Pydantic, SQLAlchemy, Alembic |
| **Veritabanı** | PostgreSQL (Supabase üzerinde barındırılan veya yerel) |
| **Kimlik doğrulama** | JWT (`python-jose`, `passlib` + bcrypt) — **Firebase kullanılmaz** |
| **AI** | OpenRouter — varsayılan model `openai/gpt-oss-120b:free` |
| **PDF** | ReportLab (+ Pillow) — sunucuda stream, kalıcı dosya yok |

**Kapsam dışı:** React Native, Firebase Auth/FCM, Redis önbellek, tekme/kasılma sayaçları, push bildirimleri.

---

## 3. Kullanıcı akışları ve fonksiyonel gereksinimler

### 3.0. Auth ve onboarding ✅

#### Web rotaları

```
/  →  /giris (token yoksa)
/giris, /kayit  →  Auth akışı
Kayıt tamamlanınca  →  /dashboard (tekrar giriş istenmez)
Token geçerliyse  →  korumalı sayfalar (AppLayout + sidebar)
```

#### Kayıt — 2 adım

| Adım | Alanlar |
|------|---------|
| 1 — Hesap | Ad soyad, e-posta (benzersiz), şifre (min. 8 karakter) |
| 2 — Gebelik | Son adet tarihi (SAT), başlangıç kilosu (kg) |

Kayıt sonrası JWT üretilir; kullanıcı doğrudan dashboard’a yönlendirilir.

#### Oturum

- Token tarayıcı **`sessionStorage`** içinde saklanır (sekme kapanınca oturum biter).
- API: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET/PATCH/DELETE /auth/me`.

---

### 3.1. Ana navigasyon ✅

Sidebar menüsü:

| Menü (UI) | Rota |
|-----------|------|
| Dashboard | `/dashboard` |
| Sağlık Takibi | `/saglik` |
| Takvim | `/takvim` |
| Kütüphane | `/kutuphane` |
| Forum | `/forum` |
| Gebelik Asistanı (Danışma AI) | `/bebegimle-konus`* |

\* Teknik URL yolu; kullanıcıya **Gebelik Asistanı — AI destekli danışma** olarak sunulur.

Üst çubukta kullanıcı menüsü ve forum bildirimleri.

---

### 3.2. Dashboard ✅

- **Geri sayım:** Beklenen doğum tarihine kalan gün.
- **Hafta/gün:** SAT üzerinden hesaplanan gebelik haftası ve gün.
- **Trimester:** 1–13 / 14–26 / 27–40+ hafta aralıkları.
- **Bebek durumu:** `weekly_metadata` tablosundan boy, kilo, meyve/nesne kıyası (`baby_size`).
- **Hero metni:** Haftalık `baby_size` ile dinamik özet cümle.
- **Özet kartları:** Son tansiyon, son kan şekeri (tarih ipucu ile), bebek bilgisi.
- **Kilo grafiği:** X ekseni ölçüm tarihi (`gg/aa`), Y ekseni kilo.
- **Yaklaşan etkinlikler:** `upcoming` API ile liste.
- **Danışma AI CTA:** Dashboard’dan Gebelik Asistanı sayfasına yönlendirme.

**API:** `GET /dashboard`, `GET /get-current-status`, `GET /pregnancy/status`.

---

### 3.3. Haftalık biyolojik veri ✅ (dashboard entegrasyonu)

- 1–42 hafta referans verisi `weekly_metadata` tablosunda (Alembic seed).
- Alanlar: `baby_weight`, `baby_length`, `baby_size`, `description`, `common_symptoms`, `tips`.
- Ayrı “haftalık rapor” sayfası yok; veriler dashboard’da gösterilir.

---

### 3.4. Sağlık veri girişi ✅

**Günlük log (`daily_logs`):** tarih, kilo, tansiyon (sistolik/diyastolik), kan şekeri, nabız, su, not.

- Ters kronolojik liste; riskli tansiyon (>140/90) görsel vurgu.
- Trend grafikleri: kilo, tansiyon, kan şekeri.
- Gelecek tarihli kayıt backend’de engellenir.

**API:** `GET/POST/PUT/DELETE /measurements`, `GET /measurements/charts`, `GET /health/measurements/summary`, `GET /health/measurements/trends/{type}`.

---

### 3.5. PDF rapor ✅

- Sağlık Takibi sayfasından tarih aralığı seçimi ile indirme.
- ReportLab ile tablo formatında PDF; sunucuda kalıcı dosya tutulmaz.

**API:** `GET /reports/pdf?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`.

---

### 3.6. Takvim ✅

- Randevu / etkinlik CRUD.
- Türkçe locale (`date-fns/locale/tr`); hafta Pazartesi’den başlar.

**API:** `GET/POST/PUT/DELETE /calendar/events`.

---

### 3.7. Kütüphane ✅

- Kategori bazlı makale listesi ve detay.
- Makale gövdesi **Markdown** olarak render edilir (`react-markdown`).
- Beğeni (like) desteği.

**API:** `GET/POST/PUT/DELETE /library/articles`, like uçları.

---

### 3.8. Forum ✅

- Soru listesi, detay, yanıt, beğeni.
- Zaman etiketi `created_at` üzerinden dinamik: Bugün / Dün / tam tarih.
- Forum etkileşimlerinde **uygulama içi** bildirimler (yorum, beğeni).

**API:** `GET/POST /forum`, `GET/PUT/DELETE /forum/questions/{id}`, yanıt ve beğeni uçları; `GET /notifications`, `PATCH /notifications/{id}/read`.

---

### 3.9. Danışma AI (Gebelik Asistanı) ✅

AI destekli danışma sohbeti; gebelik süreci, bebek gelişimi ve sağlık kayıtları hakkında bilgilendirici yanıtlar verir.

- OpenRouter üzerinden LLM; tarayıcı doğrudan modele gitmez.
- Çoklu sohbet oturumu: sol panel geçmiş, sağ panel aktif sohbet.
- Kişisel sağlık verisi yalnızca mesaj bağlamına göre seçici eklenir.
- Türkçe, destekleyici ton; teşhis/ilaç önerisi yok; riskli belirtide doktora yönlendirme.

**Arayüz:** `BabyChat.tsx` — başlık “Gebelik Asistanı”, alt metin danışma odaklı. Sidebar’da “AI destekli danışma”.

**API:** `GET/POST/DELETE /chat/sessions`, `GET/POST /chat/sessions/{id}/messages`, `POST /chat/sessions/{id}/assistant`.

Detay: [`prodocs/gebelik-asistani-mimari.md`](prodocs/gebelik-asistani-mimari.md).

---

### 3.10. Bildirimler ✅

| Özellik | Durum |
|---------|--------|
| Forum bildirimleri (yorum/beğeni) | ✅ Uygulama içi (`NotificationDropdown`) |

Push bildirimi veya harici bildirim servisi **kullanılmaz**.

---

## 4. Veri modeli (özet)

| Tablo | Amaç |
|--------|------|
| `users` | Profil, SAT, EDD, başlangıç kilosu |
| `tokens` | JWT oturum kayıtları |
| `daily_logs` | Sağlık ölçümleri |
| `weekly_metadata` | 1–42 hafta statik bebek/semptom verisi |
| `calendar_events` | Takvim etkinlikleri |
| `library_articles`, `library_likes` | Kütüphane |
| `forum_threads`, `forum_replies`, `forum_likes` | Forum |
| `notifications` | Forum bildirimleri |
| `chat_sessions`, `chat_messages` | Danışma AI sohbetleri |

Detay: [`prodocs/veritabani-yapisi.md`](prodocs/veritabani-yapisi.md).

---

## 5. Güvenlik ve gizlilik

- JWT ile kimlik doğrulama; parola bcrypt hash.
- Sağlık verileri KVKK/GDPR kapsamında hassas kabul edilir.
- Frontend doğrudan veritabanına bağlanmaz; tüm erişim FastAPI üzerinden.
- `.env` ve API anahtarları repoya eklenmez.

---

## 6. Tasarım (UI/UX)

Renk ve ekran eşleşmeleri [`DesignSystem.md`](DesignSystem.md) dosyasında tanımlıdır.

| Öğe | Renk |
|-----|------|
| Arka plan | `#F4F7F9` |
| Primary (sidebar, butonlar) | `#6797B2` |
| Danışma AI butonu | `#FFA0A5` |
| Metin | `#B25E63` |

Light mode; sidebar + responsive layout.

---

## 7. Uç durumlar

| Durum | Beklenen davranış |
|--------|-------------------|
| Gelecek tarihli sağlık kaydı | Engellenir |
| Doğum tarihi geçti | 40+ hafta gösterimi |
| `weekly_metadata` kaydı yok | “Bilgi bulunamadı” |
| OpenRouter anahtarı yok | Sohbet 503 |
| PDF aralığında kayıt yok | 404 |

---

## 8. Başarı metrikleri (KPI)

- Günlük/haftalık sağlık verisi giriş oranı
- Dashboard ve Danışma AI oturum süresi
- Forum etkileşimi (soru, yanıt, beğeni)
- PDF rapor indirme sayısı
- Kayıt → dashboard tamamlama oranı

---

## 9. MVP dışı / sonraki sürüm

- Birim dönüşümü (cm/gr ↔ inch/lb)
- Gelişmiş forum moderasyon paneli
- Mobil native uygulama (React Native)
- E2E test ve CI/CD otomasyonu

---

> **Not:** İlk PRD sürümü React Native, Firebase Auth, tekme/kasılma sayaçları ve FCM bildirimleri öngörüyordu. Güncel ürün **Vite + React web uygulaması**dır; kimlik doğrulama JWT, bildirimler yalnızca uygulama içi forum bildirimleridir.
