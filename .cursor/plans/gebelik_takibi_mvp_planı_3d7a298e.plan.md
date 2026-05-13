---
name: Gebelik Takibi MVP Planı
overview: PRD ve MVP kapsamına göre kimlik doğrulama, temel takip modülleri, sayaçlar, içerik, raporlama ve kalite güvence adımlarını içeren aşamalı bir geliştirme yol haritası.
todos:
  - id: phase0-setup
    content: Teknoloji stack, domain model ve CI/lint/test iskeletini netleştir
    status: completed
  - id: phase1-auth
    content: Auth + 2 adımlı onboarding + session persistence akışlarını tamamla
    status: completed
  - id: phase2-dashboard
    content: Gebelik hesaplama motoru ve dashboard kartlarını uçtan uca çıkar
    status: completed
  - id: phase3-healthlogs
    content: Kilo/tansiyon loglama, trend API ve risk işaretleme kurallarını ekle
    status: completed
  - id: phase4-counters
    content: Tekme ve kasılma sayaçları ile 5-1-1 uyarı algoritmasını bitir
    status: completed
  - id: phase5-content-forum
    content: Haftalık metadata, kütüphane araması ve temel forum/moderasyon akışını tamamla
    status: completed
  - id: phase6-report-notify
    content: PDF export ve temel bildirimleri devreye al
    status: completed
  - id: phase7-qa-release
    content: Testler, güvenlik/uyum kontrolleri ve pilot yayın hazırlığını tamamla
    status: completed
isProject: false
---

# Gebelik Takibi MVP Geliştirme Planı

## Kapsam ve Öncelik

- Ana kaynaklar: [c:/Users/CASPER/Desktop/gebetakip/PRD.md](c:/Users/CASPER/Desktop/gebetakip/PRD.md), [c:/Users/CASPER/Desktop/gebetakip/MVP.md](c:/Users/CASPER/Desktop/gebetakip/MVP.md)
- `Must-have` (MVP çekirdeği): Auth + onboarding, dashboard hesaplamaları, kilo/tansiyon loglama, tekme/kasılma sayaçları, haftalık biyolojik veri, temel kütüphane+arama, temel forum, PDF export.
- `Should-have` (MVP sonu): bildirim altyapısı (en az lokal), raporlama iyileştirmeleri, forum moderasyon akışı.
- `Later` (MVP sonrası): çoklu birim dönüşümü (cm/gr ↔ inch/lb), gelişmiş moderasyon, medya destekli notlar.

## Faz 0 — Mimari ve Proje Kurulumu (3-4 gün)

- Frontend ve backend teknolojisini netleştir: React Native + Node/Express + PostgreSQL (PRD önerisiyle uyumlu).
- Ortak domain modeli çıkar: kullanıcı, gebelik günü/hafta, günlük sağlık logları, sayaç logları, haftalık statik metadata.
- Ortamlar: local/dev/staging ayrımı, temel CI (lint + test), secrets yönetimi.
- Başlangıç güvenlik çerçevesi: JWT yaşam döngüsü, şifre hashleme, temel rate limit, hassas veri sınıflandırması.

## Faz 1 — Kimlik Doğrulama ve Onboarding (1 hafta)

- Auth stack ve main stack navigasyonunu ayır.
- Akışlar:
  - AuthGate (`Giriş Yap` / `Üye Ol`)
  - Login (email+şifre)
  - Register Step 1 (ad-soyad, email, şifre)
  - Register Step 2 (SAT veya EDD, başlangıç kilosu)
- Backend endpointleri: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`.
- Session persistence: token geçerliyse doğrudan main stack’e giriş.
- Kritik kabul kriteri: kayıt adım 2 sonrası kullanıcı login’e dönmeden ana akışa düşmeli.

## Faz 2 — Hesaplama Motoru ve Dashboard (1 hafta)

- Core hesaplama servisi:
  - SAT/EDD normalizasyonu
  - gebelik günü, hafta+gün, trimester, kalan gün
  - edge case: 40+ hafta davranışı
- Dashboard kartları:
  - hafta/gün, trimester, geri sayım
  - son kilo ve son tansiyon widget’ları
- API: `GET /get-current-status` ve dashboard için gerekli birleşik veri response’u.

## Faz 3 — Sağlık Verisi Modülü (1 hafta)

- Kilo loglama + trend line chart verisi.
- Tansiyon loglama (sistolik/diyastolik/nabız) + ters kronolojik liste.
- Risk işaretleme kuralı: >140/90 görsel uyarı.
- Gelecek tarihli veri girişini backend ve frontend seviyesinde engelle.
- API: `GET /health-trends` ile grafik uyumlu JSON.

## Faz 4 — Sayaçlar (Tekme/Kasılma) (1 hafta)

- Tekme sayacı: oturum başlatma, dokunuş logları, 1 saat sonunda kayıt.
- Kasılma kronometresi: start/stop ile duration ve frequency hesaplama.
- `5-1-1` kuralı tespit edildiğinde kritik uyarı.
- API: `POST /analyze-contraction` ve geçmiş sayaç oturumları endpointi.

## Faz 5 — İçerik, Kütüphane ve Forum (1 hafta)

- Haftalık biyolojik metadata (1-42 hafta) seed/import mekanizması.
- Kütüphane: kategori bazlı listeleme + metin arama.
- Forum: thread listesi, detay, yorum, kategorileme, `report` aksiyonu (temel moderasyon flag).
- Performans için temel indeksleme (hafta, kullanıcı, tarih, kategori).

## Faz 6 — PDF Raporlama ve Bildirimler (4-5 gün)

- PDF export: kilo+tansiyon+notlar için doktor paylaşımına uygun çıktı.
- Sunucuda kalıcı dosya tutmama: stream veya kısa ömürlü geçici URL stratejisi.
- Bildirimler:
  - minimum: lokal su hatırlatıcıları
  - opsiyonel MVP sonu: yeni hafta için server-side tetik.

## Faz 7 — Kalite, Uyum ve Yayın Hazırlığı (1 hafta)

- Test kapsamı:
  - unit: hesaplama motoru, 5-1-1 analizi
  - integration: auth/onboarding, log endpointleri
  - e2e: ilk kurulumdan dashboard’a kadar ana akış
- Güvenlik/uyum kontrol listesi:
  - at-rest encryption stratejisi (DB/kolon seviyesi)
  - KVKK/GDPR veri saklama ve silme politikası
- Ürün metrikleri:
  - DAU veri girişi
  - sayaç sonrası retention
  - PDF conversion
- Pilot kullanıcı ile soft launch ve hataların triage edilmesi.

## Sprint Planı (Öneri)

- Sprint 1: Faz 0 + Faz 1
- Sprint 2: Faz 2 + Faz 3
- Sprint 3: Faz 4 + Faz 5
- Sprint 4: Faz 6 + Faz 7 + stabilizasyon

## Bağımlılıklar ve Riskler

- Haftalık biyolojik veri setinin doğruluğu gecikirse dashboard değeri düşer; erken doğrulanmalı.
- Auth + onboarding tamamlanmadan diğer modüllerin kullanıcı bazlı testi sağlıklı yapılamaz.
- PDF motoru ve mobilde chart performansı erken POC ile test edilmeli.
- Forum kötüye kullanım riskine karşı en azından `report` ve admin görünürlüğü MVP’ye dahil edilmeli.

