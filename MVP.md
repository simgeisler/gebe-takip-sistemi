# 📄 Ürün Kapsam Dökümanı: Gebelik Takibi (MVP)

**Ürün Sloganı:** "Haftalık Veri, Sağlık Kaydı ve Teknik Süreç Yönetimi."  
**Hedef Kitle:** 20-36 yaş arası, gebelik sürecini verilerle takip etmek isteyen kullanıcılar.

## 1. Ürün Vizyonu
Gebelik Takibi, gebelik sürecini karmaşadan arındırarak; biyolojik evreler, tıbbi gereklilikler ve kişisel sağlık parametreleri üzerinden takip etmeyi sağlayan, yüksek işlevli bir dijital kayıt defteridir.

## 2. Fonksiyonel Gereksinimler (MVP Özellikleri)

### 2.1. Teknik Durum Paneli (Dashboard)
**Tanım:** Mevcut gebelik statüsünün sayısal özeti.  
**Detaylar:**
* Kaçıncı hafta ve gün olduğu bilgisi.
* Doğuma kalan gün sayısı (Numerik geri sayım).
* Mevcut trimester (1, 2 veya 3) göstergesi.

### 2.2. Haftalık Biyolojik Rapor
**Tanım:** Bebeğin ve annenin fiziksel değişimlerini açıklayan teknik veri alanı.  
**Detaylar:**
* **Gelişim Verisi:** Bebeğin tahmini boy (cm) ve ağırlık (gr) bilgileri ile o hafta tamamlanan organ gelişimleri.
* **Semptom Analizi:** Annede oluşabilecek fiziksel değişimler ve tıbbi nedenleri.

### 2.3. Teknik Boyut Kıyaslayıcı
**Tanım:** Bebeğin hacmini nesnel objelerle somutlaştırma.  
**Detaylar:** Haftalık değişen standart nesne kıyaslamaları (Örn: "Bebeğiniz şu an bir greyfurt boyutundadır").

### 2.4. Sağlık Veri Girişi ve Loglama
**Tanım:** Biyometrik verilerin grafiksel takibi.  
**Detaylar:**
* **Kilo Kaydı:** Başlangıç kilosuna göre artış trendini gösteren çizelge.
* **Tansiyon Kaydı:** Sistolik ve diyastolik değerlerin tarih/saat bazlı listelenmesi.

### 2.5. Operasyonel Sayaçlar
**Tanım:** Süreç içindeki hayati hareketlerin ölçülmesi.  
**Detaylar:**
* **Tekme Sayacı:** Hareket sıklığının teknik kaydı.
* **Kasılma Kronometresi:** Sancı aralıklarını ve sürelerini ölçen, doğum başlangıcını analiz eden araç.

### 2.6. Rutin Hatırlatıcılar
**Tanım:** Günlük ve periyodik görev bildirimleri.  
**Detaylar:** Su tüketimi, ilaç/vitamin dozları ve tıbbi randevu takvimi uyarıları.

### 2.7. Teknik Veri Raporu (PDF Export)
**Tanım:** Uygulama verilerinin tıbbi bir dökümana dönüştürülmesi.  
**Detaylar:** Girilen tüm sağlık verilerinin (kilo, tansiyon, notlar) doktor incelemesine uygun, profesyonel bir tablo halinde PDF çıktısının alınması.

### 2.8. Bilgi Setleri (Teknik Kütüphane)
**Tanım:** Konu başlıklarına göre ayrılmış rehber metinler.  
**Detaylar:** Beslenme yasakları, yapılması gereken tıbbi testler listesi, fiziksel aktivite limitleri ve yasal haklar (izin süreçleri).

### 2.9. Tartışma ve Bilgi Paylaşım Forumu
**Tanım:** Kullanıcılar arası bilgi alışverişi alanı.  
**Detaylar:** Kategorize edilmiş (Hastaneler, Doktorlar, Ekipmanlar) başlıklar üzerinden soru-cevap akışı.

### 2.10. Süreç Kaydı ve Notlar
**Tanım:** Teknik veya kişisel notların kronolojik saklanması.  
**Detaylar:** Günlük not girişi ve opsiyonel fotoğraf (gelişim takibi için) ekleme özelliği.

## 3. Tasarım ve Kullanıcı Deneyimi (UX/UI)
* **Renk Paleti:** Beyaz, Koyu Gri ve profesyonel bir Sağlık Mavisi (Medical Blue). Göz yormayan, yüksek kontrastlı renkler.
* **Navigasyon:** Hızlı veri girişi odaklı, 5 sekmeli alt menü yapısı.
* **Dil:** Net, mesafeli, bilgilendirici ve profesyonel bir terminoloji.