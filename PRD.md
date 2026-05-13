# PRD: Gebelik Takibi MVP

**Ürün Sloganı:** Haftalık Veri, Sağlık Kaydı ve Teknik Süreç Yönetimi  
**Versiyon:** 1.0 (MVP)  
**Durum:** Taslak / Geliştirmeye Hazır

---

## 1. Ürün Özeti ve Hedefler

Bu ürünün amacı, **20-36 yaş arası** hamile bireylere, süreci duygusal bir günlükten ziyade veri odaklı, tıbbi bir takip paneli olarak sunmaktır. MVP'nin başarısı; veri giriş hızı, grafiksel doğruluk ve raporlama kalitesiyle ölçülecektir.

---

## 2. Kullanıcı Akışları ve Fonksiyonel Gereksinimler

### 2.0. Auth & Onboarding Akışı ★ YENİ

#### Navigation Stack Özeti

```
App Start
  └── JWT token kontrolü
        ├── Token geçerliyse       → Main Stack (TabNavigator)
        └── Token yoksa/geçersizse → Auth Stack
              ├── AuthGateScreen       (Giriş Yap / Üye Ol seçimi)
              ├── LoginScreen          (Email + Şifre)
              └── RegisterScreen
                    ├── Step 1: HesapBilgileri   (Ad Soyad, Email, Şifre)
                    └── Step 2: GebelikBilgileri  (SAT, Başlangıç Kilosu)
                          └── → Direkt Main Stack'e yönlendir (tekrar login isteme)

Main Stack
  └── TabNavigator
        ├── Dashboard
        ├── Takip      (Kilo, Tansiyon)
        ├── Sayaçlar   (Tekme, Kasılma)
        ├── Forum
        └── Kütüphane
```

#### 2.0.1. Karşılama Ekranı (Auth Gate)

Uygulama ilk açıldığında kullanıcıya tek bir seçim ekranı gösterilir. Bu ekran iki aksiyona sahiptir:

* **Giriş Yap** — Mevcut hesabıyla devam eden kullanıcılar için.
* **Üye Ol** — Uygulamayı ilk kez kullanan yeni kullanıcılar için.

#### 2.0.2. Üye Ol Akışı — 2 Adımlı Onboarding

Kayıt süreci iki ayrı ekrana bölünür. Kullanıcı her iki adımı tamamladıktan sonra tekrar login ekranına yönlendirilmeden doğrudan Ana Ekran'a (Main Stack) geçer.

| Adım | Ekran Adı | Toplanan Alanlar |
|------|-----------|-----------------|
| Adım 1 | Hesap Bilgileri | Ad Soyad (zorunlu), E-posta adresi (zorunlu, unique), Şifre (min. 8 karakter) |
| Adım 2 | Gebelik Bilgileri | Son Adet Tarihi (SAT) veya Beklenen Doğum Tarihi, Başlangıç kilosu (kg) |

> **Önemli:** Adım 2 tamamlandıktan sonra kullanıcı tekrar Giriş Yap ekranına yönlendirilmez. JWT token üretilir ve kullanıcı doğrudan Ana Ekran'a (TabNavigator) yönlendirilir.

#### 2.0.3. Giriş Yap Akışı

* Kullanıcı e-posta ve şifresini girer.
* Backend kimlik doğrulaması yapar; JWT token döner.
* Token, cihazda güvenli şekilde saklanır (Secure Storage / Keychain).
* Kullanıcı, daha önce girdiği SAT/profil verisine göre hesaplamalar yapılarak kendi Dashboard ekranına yönlendirilir.

#### 2.0.4. Oturum Sürekliliği (Session Persistence)

Kullanıcı uygulamayı kapatıp tekrar açtığında sistem şu kontrolü yapar:

* **JWT token geçerli →** Auth Stack atlanır, doğrudan Main Stack (TabNavigator) açılır.
* **JWT token süresi dolmuş veya yok →** Auth Gate ekranına yönlendirilir.

#### 2.0.5. Teknik Gereksinimler (Auth)

* **Authentication:** JWT (JSON Web Token) ile session yönetimi.
* **Token Saklama:** React Native SecureStore (Expo) veya Keychain (iOS) / Keystore (Android).
* **API Endpoint'leri:**
  * `POST /auth/register` — Adım 1 + Adım 2 verilerini alır, kullanıcı oluşturur, JWT döner.
  * `POST /auth/login` — Email + Şifre doğrular, JWT döner.
  * `POST /auth/logout` — Token'ı geçersiz kılar.
  * `GET /auth/me` — Token doğrulama ve kullanıcı bilgisi döner.
* **Validation:** E-posta benzersizliği kayıt sırasında kontrol edilmeli; aynı e-posta ile kayıt engellenmeli.
* **Hata Mesajları:** "Bu e-posta zaten kayıtlı", "Hatalı e-posta veya şifre" gibi kullanıcıya açık mesajlar gösterilmeli.

---

### 2.1. Onboarding & Profil Oluşturma (Kritik Altyapı)

* **Gereksinim:** Kullanıcıdan "Son Adet Tarihi (SAT)" veya "Beklenen Doğum Tarihi" alınmalıdır.
* **Mantık:** Sistem, tüm haftalık hesaplamaları SAT üzerinden **+280 gün** formülüyle yapacaktır.

### 2.2. Teknik Durum Paneli (Dashboard)

* **Geri Sayım:** Mevcut tarih ile beklenen doğum tarihi arasındaki gün farkı.
* **Hafta/Gün Hesaplama:** `Hafta = floor((Bugün - SAT) / 7)` — Örn: 24 hafta 3 gün.
* **Trimester Mantığı:**
  * 1. Trimester: 1-13. haftalar
  * 2. Trimester: 14-26. haftalar
  * 3. Trimester: 27-40+ haftalar
* **UI Gereksinimi:** Dashboard açıldığında en güncel "Kilo" ve "Tansiyon" verisi küçük widget'lar olarak görünmelidir.

### 2.3. Haftalık Biyolojik Rapor ve Kıyaslayıcı

* **Veri Yapısı:** Her hafta (1'den 42'ye kadar) için DB'de tanımlı; Boy (cm), Ağırlık (gr), Organ Gelişimi metni ve Semptom Analizi metni bulunmalıdır.
* **Boyut Kıyaslama:** Görsel bir obje (meyve/sebze/nesne) ile haftalık eşleşme.
  * *Örnek:* 8. Hafta = Ahududu, 24. Hafta = Mısır.

### 2.4. Sağlık Veri Girişi (Loglama)

* **Kilo Takibi:** Başlangıç kilosu (profilde tanımlanan) baz alınır. Giriş yapılan her veri, X ekseni "Zaman", Y ekseni "Kilo" olan bir **line-chart** üzerinde gösterilir.
* **Tansiyon Takibi:**
  * **Giriş:** Sistolik (Büyük), Diyastolik (Küçük) ve Nabız (Opsiyonel).
  * **Listeleme:** Ters kronolojik sırada (en yeni üstte). Riskli değerler (>140/90) kırmızı vurguyla işaretlenmelidir.

### 2.5. Operasyonel Sayaçlar (Real-time Tools)

* **Tekme Sayacı:** "Başlat" butonuyla aktif olur. Her dokunuş bir log oluşturur. 1 saatlik oturum sonunda toplam sayı kaydedilir.
* **Kasılma Kronometresi:** Start/Stop mekanizması. Sistem; iki kasılma arasındaki sıklığı (*frequency*) ve kasılmanın kendi süresini (*duration*) hesaplar.
* **Algoritma:** Eğer kasılmalar 5 dakikada bir geliyorsa ve 1 dakika sürüyorsa (**5-1-1 kuralı**), ekranda "Hastaneye gitme vaktiniz gelmiş olabilir" uyarısı tetiklenmelidir.

### 2.6. Bilgi Setleri & Kütüphane

* **Kategorizasyon:** Beslenme, Testler, Aktivite, Yasal Haklar.
* **Arama:** Metin tabanlı arama (*search bar*) MVP'ye dahil edilmelidir.

### 2.7. Tartışma Forumu

* **Yapı:** Reddit benzeri basit bir thread yapısı.
* **Kategoriler:** Hastane Önerileri, Doktor Yorumları, Ürün Tavsiyeleri.
* **Moderasyon:** "Şikayet et" (*report*) butonu teknik olarak bulunmalıdır.

---

## 3. Teknik Gereksinimler

### 3.1. Veri Modeli ve Veritabanı Mimarisi (Schema)

* **User Profile:** `user_id`, `name`, `email`, `password_hash`, `expected_due_date`, `last_menstrual_period`, `starting_weight`, `created_at`.
* **Auth Tokens:** `token_id`, `user_id`, `token_hash`, `expires_at`, `device_info`.
* **Daily Logs Table:** `log_id`, `user_id`, `date`, `weight`, `systolic`, `diastolic`, `water_intake`, `note`.
* **Weekly Metadata (Static):** `week_number`, `fetus_size_cm`, `fetus_weight_gr`, `development_milestones` (JSON), `comparison_object_name`, `image_url`.
* **Counter Logs:** `counter_id`, `user_id`, `type` (kick/contraction), `start_time`, `end_time`, `duration_seconds`, `frequency_seconds`.

### 3.2. API ve Backend Mantığı (Business Logic)

* **Auth Endpoints:** `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`.
* **Calculation Engine:** `GET /get-current-status` — Hafta, gün ve trimester bilgisini döner.
* **Health Analytics API:** `GET /health-trends` — Kilo ve tansiyon verilerini grafik kütüphanelerine uygun JSON formatında hazırlar.
* **Contraction Analyzer:** `POST /analyze-contraction` — Son 1 saatteki kasılma sıklığını analiz eder. Danger zone tespiti yapar.

### 3.3. PDF Üretim Motoru (Reporting Service)

* **Kütüphane:** Puppeteer veya ReportLab (Python) kullanılmalıdır.
* **İşleyiş:** PDF'ler sunucuda saklanmamalı, doğrudan stream edilmeli veya geçici bir S3 bucket üzerinden sunulmalıdır.

### 3.4. Bildirim Altyapısı (Push Notifications)

* **Servis:** Firebase Cloud Messaging (FCM).
* **Trigger:** Lokal su hatırlatıcıları ve Server-side cron job (Yeni hafta bildirimleri).

### 3.5. Güvenlik ve Gizlilik (Compliance)

* **Veri Hassasiyeti:** Sağlık verileri GDPR ve KVKK kapsamında "Özel Nitelikli Kişisel Veri" statüsündedir.
* **Encryption:** Veritabanında veriler *at-rest* (**AES-256**) olarak şifrelenmelidir.
* **Authentication:** **JWT** (JSON Web Token) ile session yönetimi.

### 3.6. Uç Durumlar (Edge Cases)

* **Gelecek Tarihli Veri Girişi:** İleri tarihli veri girişi engellenmelidir.
* **Negatif Geri Sayım:** Doğum tarihi geçtiğinde "40+ hafta" gösterilmeli ve "Doğum gerçekleşti mi?" butonu aktif edilmelidir.
* **Birim Dönüşümleri:** Mimaride cm/gr ve inch/lb esnekliği sağlanmalıdır.

### 3.7. MVP Teknoloji Stack Önerisi

* **Frontend:** React Native veya Flutter.
* **Backend:** Node.js (Express) veya Python (FastAPI).
* **Database:** PostgreSQL.
* **Caching:** Redis.

---

## 4. Tasarım Parametreleri (UI/UX)

* **Tema:** Light Mode. White (`#FFFFFF`) zemin, Medical Blue (`#0057B8`) butonlar, Dark Gray (`#333333`) metinler.
* **Erişilebilirlik:** Minimum **16px** font boyutu.
* **Navigasyon:** Dashboard | Takip | Sayaçlar | Forum | Kütüphane.

---

## 5. Başarı Metrikleri (KPIs)

* **DAU:** Veri girişi yapan kullanıcı oranı.
* **Retention:** Sayaç kullanımı sonrası geri dönüş oranı.
* **Conversion:** Üretilen PDF raporu sayısı.

---

> **Developer Notu:** Veritabanı mimarisinde "Gebelikteki Gün" bilgisini ana anahtar (*key*) olarak kullanın. Tüm hesaplamalar bu gün sayısına göre tetiklenecektir. Auth akışında kullanıcının ilk kaydında Adım 2'den sonra token üretilmeli ve kullanıcı doğrudan Ana Ekran'a düşmelidir.
