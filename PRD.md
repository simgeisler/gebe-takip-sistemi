# PRD: Gebelik Takibi MVP

**Ürün Sloganı:** Haftalık Veri, Sağlık Kaydı ve Teknik Süreç Yönetimi  
**Versiyon:** 1.0 (MVP)  
**Durum:** Taslak / Geliştirmeye Hazır  

---

## 1. Ürün Özeti ve Hedefler
Bu ürünün amacı, **20-36 yaş arası** hamile bireylere, süreci duygusal bir günlükten ziyade veri odaklı, tıbbi bir takip paneli olarak sunmaktır. MVP'nin başarısı; veri giriş hızı, grafiksel doğruluk ve raporlama kalitesiyle ölçülecektir.

---

## 2. Kullanıcı Akışları ve Fonksiyonel Gereksinimler

### 2.1. Onboarding & Profil Oluşturma (Kritik Altyapı)
* **Gereksinim:** Kullanıcıdan "Son Adet Tarihi (SAT)" veya "Beklenen Doğum Tarihi" alınmalıdır.
* **Mantık:** Sistem, tüm haftalık hesaplamaları SAT üzerinden **+280 gün** formülüyle yapacaktır.

### 2.2. Teknik Durum Paneli (Dashboard)
* **Geri Sayım:** Mevcut tarih ile beklenen doğum tarihi arasındaki gün farkı.
* **Hafta/Gün Hesaplama:** $Hafta = \lfloor (Bugün - SAT) / 7 \rfloor$ (Örn: 24 hafta 3 gün).
* **Trimester Mantığı:** * 1. Trimester: 1-13. haftalar
    * 2. Trimester: 14-26. haftalar
    * 3. Trimester: 27-40+ haftalar
* **UI Gereksinimi:** Dashboard açıldığında en güncel "Kilo" ve "Tansiyon" verisi küçük widget'lar olarak görünmelidir.

### 2.3. Haftalık Biyolojik Rapor ve Kıyaslayıcı
* **Veri Yapısı:** Her hafta (1'den 42'ye kadar) için DB'de tanımlı; Boy (cm), Ağırlık (gr), Organ Gelişimi metni ve Semptom Analizi metni bulunmalıdır.
* **Boyut Kıyaslama:** Görsel bir obje (meyve/sebze/nesne) ile haftalık eşleşme.
    * *Örnek:* 8. Hafta = Ahududu, 24. Hafta = Mısır.

### 2.4. Sağlık Veri Girişi (Loglama)
* **Kilo Takibi:** Başlangıç kilosu (profilde tanımlanan) baz alınır. Giriş yapılan her veri, X ekseni "Zaman", Y ekseni "Kilo" olan bir **line-chart** üzerinde gösterilir.
* **Tansiyon Takibi:** * **Giriş:** Sistolik (Büyük), Diyastolik (Küçük) ve Nabız (Opsiyonel).
    * **Listeleme:** Ters kronolojik sırada (en yeni üstte). Riskli değerler (Örn: >140/90) kırmızı vurguyla işaretlenmelidir.

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
Uygulamanın kalbi, zaman tabanlı bir yapı olan **"Gebelik Günü"** üzerine kurulmalıdır.
* **User Profile:** `user_id`, `email`, `expected_due_date`, `last_menstrual_period`, `starting_weight`.
* **Daily Logs Table:** `log_id`, `user_id`, `date`, `weight`, `systolic`, `diastolic`, `water_intake`, `note`.
* **Weekly Metadata (Static):** `week_number`, `fetus_size_cm`, `fetus_weight_gr`, `development_milestones` (JSON), `comparison_object_name`, `image_url`.
* **Counter Logs:** `counter_id`, `user_id`, `type` (kick/contraction), `start_time`, `end_time`, `duration_seconds`, `frequency_seconds`.

### 3.2. API ve Backend Mantığı (Business Logic)
* **Calculation Engine:** `GET /get-current-status`: Hafta, gün ve trimester bilgisini döner.
* **Health Analytics API:** `GET /health-trends`: Kilo ve tansiyon verilerini grafik kütüphanelerine uygun JSON formatında hazırlar.
* **Contraction Analyzer:** `POST /analyze-contraction`: Son 1 saatteki kasılma sıklığını analiz eder. Danger zone tespiti yapar.

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
> **Developer Notu:** Veritabanı mimarisinde "Gebelikteki Gün" bilgisini ana anahtar (*key*) olarak kullanın. Tüm hesaplamalar bu gün sayısına göre tetiklenecektir.