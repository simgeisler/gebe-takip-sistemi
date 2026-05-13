# Gebelik Takip Sistemi: Web Uygulaması Tasarım ve Fonksiyon Dökümanı

Bu döküman, Gebelik Takip Sistemi web uygulamasının görsel kimliğini, kullanıcı akışlarını ve modül detaylarını tanımlar.

---

## 🎨 Renk Paleti Uygulama Rehberi

Tasarımda görsel uyumu ve kullanıcı deneyimini (UX) ön planda tutan belirlenmiş renk paleti:

| Öğe | Renk Kodu | Kullanım Alanı |
| :--- | :--- | :--- |
| **Background** | `#F4F7F9` | Göz yormayan açık mavi/gri ton. Tüm sayfa arka planlarında kullanılır. |
| **Primary** | `#6797B2` | Dengeli ve profesyonel mavi. Ana butonlar, Sidebar ve navigasyon. |
| **Secondary** | `#FFA0A5` | Sıcak, dikkat çekici pastel pembe. **AI (Bebeğimle Konuş)** butonu. |
| **Accent** | `#6CA9CC` / `#E886BC` | Detaylar, grafik barları ve takvim etkinlikleri. |
| **Text** | `#B25E63` | Koyu tonlarda, derinlik katan premium metin rengi. |

---

## 1. Auth & Onboarding (Giriş & Kayıt Akışı)

Kullanıcının sisteme ilk temas noktası olan bu aşama, sade ve güven verici bir tasarıma sahiptir.

| Ekran | Fonksiyon | Görsel & Stil Detayları |
| :--- | :--- | :--- |
| **Giriş (Login)** | Kullanıcı e-posta/şifre girişi yapar. | Arka plan `#F4F7F9`. Buton `#6797B2`. Kart beyaz. |
| **Kayıt (Step 1)** | Ad-Soyad, Email, Şifre toplama. | 2 aşamalı progress bar. Metinler `#B25E63`. |
| **Kayıt (Step 2)** | SAT ve Başlangıç kilosu girişi. | Takvim picker (Date Picker). Giriş sonrası direkt Dashboard. |

---

## 2. Dashboard & Ana Navigasyon

Uygulamanın kalbi. Kullanıcı login sonrası tüm verilere buradan erişir.

| Modül | İşlev | Görsel Eşleşme |
| :--- | :--- | :--- |
| **Sidebar** | Tüm modüller arası geçiş sağlayan ana menü. | Arka plan `#6797B2` (Primary). |
| **Dashboard** | Geri sayım, hafta bilgisi, bebek durumu özeti. | Kartlar beyaz, başlık ve metinler `#B25E63`. |
| **Bebeğimle Konuş** | AI Companion (Yapay Zeka) etkileşimi. | Buton: `#FFA0A5`. Sidebar'ın en altında sabit. |

---

## 3. Ekran & Fonksiyon Eşleşme Tablosu

| Ekran | Temel Fonksiyon | Web Arayüzü Detayı |
| :--- | :--- | :--- |
| **Dashboard** | Genel durum ve özet paneli. | 3 sütunlu grid yapısı (Geri sayım, Durum, Grafik). |
| **Sağlık Takibi** | Veri girişi ve PDF Raporlama. | Sol: Form alanı. Sağ: `#6CA9CC` renkli grafikler. |
| **Takvim** | Randevu ve İlaç hatırlatıcılar. | Haftalık görünüm, `#E886BC` renkli randevu blokları. |
| **Kütüphane** | Bilgi ve rehberlik metinleri. | Kartlı ızgara (Grid) yapısı. |
| **Forum** | Topluluk başlıkları ve tartışma. | Reddit stili, geniş ve odaklanmış okuma alanı. |

---

## 4. Tasarım Kuralları ve UX Prensipleri

### 🔘 Buton Standartları
* **Genel Aksiyonlar:** Tüm ana aksiyon butonları (PDF Oluştur, Giriş Yap, Kaydet) `#6797B2` rengindedir. 
* **Hover Etkisi:** Fare ile üzerine gelindiğinde buton rengi bir ton koyulaşarak etkileşim hissi verir.

### 🤖 AI Etkileşimi (Bebeğimle Konuş)
* **Konumlandırma:** Sidebar'ın en altında kullanıcıyla sürekli temas halinde olması için sabitlenmiştir.
* **Görsel Stil:** `#FFA0A5` rengiyle "bebek/duygusal bağ" temasını vurgular. Etrafında hafif bir gölge (shadow) bulunarak derinlik kazandırılır.

### ✍️ Tipografi ve Metinler
* **Renk:** Tüm başlıklar ve gövde metinleri `#B25E63` rengiyle yazılır.
* **Hava:** Bu sofistike ton, uygulamanın "premium" ve sıcak marka kimliğini destekler.

### 📊 Veri Görselleştirme
* **Grafikler:** Sağlık takibindeki tüm çizelge ve grafikler `#6CA9CC` (Accent) rengindedir. Bu renk, mavi tonlarıyla uyumlu olup okunabilirliği en üst seviyeye çıkarır.