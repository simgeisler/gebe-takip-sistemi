# Gebelik Takip — İlerleme Günlüğü

---

## Oturum: Backend Kurulumu, Dashboard Özet Kartları (3 Haziran 2026)

### Yaklaşım

- **Backend:** FastAPI + SQLAlchemy + Alembic; API `/api/v1` altında, sağlık verileri `daily_logs` tablosunda.
- **Frontend:** React (Vite) dashboard; özet kartları backend `build_dashboard()` yanıtından (`summary_cards`) geliyor.
- **Sorun giderme:** Python import çakışmalarında dosya/klasör adı çakışmasını ayırarak çözdük (`models.py` vs `models/`).
- **Dashboard metrikleri:** Su yerine kan şekeri; tansiyon ve kan şekerinde alt satırda son ölçüm tarihi.

---

### Adım 1 — Backend açılmıyordu (`ModuleNotFoundError`)

**Belirti:** `alembic upgrade head` ve `uvicorn` şu hatayı veriyordu:

```
ModuleNotFoundError: No module named 'app.models.entities'; 'app.models' is not a package
```

**Kök neden:** Aynı isimde hem dosya hem klasör vardı:
- `app/models.py` ↔ `app/models/entities.py`
- `app/schemas.py` ↔ `app/schemas/*.py`

Python önce `.py` dosyasını modül saydığı için `app.models.entities` import edilemiyordu.

**Yapılanlar:**
1. `app/models.py` → `app/legacy_models.py` taşındı
2. `app/schemas.py` → `app/legacy_schemas.py` taşındı
3. `app/models/__init__.py` eklendi (entities + legacy re-export)
4. `app/schemas/__init__.py` eklendi (legacy şemalar re-export)

**Sonuç:** `from app.main import app` başarılı; `alembic upgrade head` çalıştı.

---

### Adım 2 — Kök URL 404 (`/` ve `/favicon.ico`)

**Belirti:** Tarayıcı `http://127.0.0.1:8000` açınca terminalde `GET /` ve `GET /favicon.ico` → 404. `/docs` → 200 (API sağlıklıydı).

**Yapılanlar (`app/main.py`):**
- `GET /` → `/docs` yönlendirmesi (307)
- `GET /favicon.ico` → 204 (boş cevap, hata yok)

**Sonuç:** Kök adres açılınca Swagger dokümantasyonuna gidiliyor.

---

### Adım 3 — Dashboard: “Bugünkü Su” → “Son Kan Şekeri”

**İstek:** Üçüncü özet kartında su yerine sağlık takibindeki son kan şekeri değeri gösterilsin.

**Yapılanlar:**

| Katman | Dosya | Değişiklik |
|--------|--------|------------|
| Backend | `app/services/ui_service.py` | `water` kartı kaldırıldı; `daily_logs.blood_glucose` son kayıt okunuyor |
| Backend | Aynı | Kart: label `Son Kan Şekeri`, value örn. `92 mg/dL`, hint `Son ölçüm · GG.AA.YYYY` |
| Frontend | `frontend/src/pages/Dashboard.tsx` | `summary_cards.blood_glucose` kullanılıyor; ikon `Activity` |

Veri kaynağı: Sağlık Takibi formundaki kan şekeri alanı (`blood_glucose`) — tansiyonla aynı `DailyLog` tablosu.

---

### Adım 4 — Dashboard: Son Tansiyon’a tarih eklendi

**İstek:** Son Tansiyon kartı, kan şekerindeki gibi son ölçüm tarihini göstersin.

**Yapılanlar (`app/services/ui_service.py`):**
- Kayıt varsa hint: `Son ölçüm · GG.AA.YYYY`
- Kayıt yoksa: `Henüz kayıt yok`

Frontend değişikliği gerekmedi; `bp_hint` zaten API’den geliyor.

---

### Mevcut durum

| Bileşen | Durum |
|---------|--------|
| Backend (`uvicorn` :8000) | Çalışır — import ve migration sorunları giderildi |
| Frontend (`npm run dev`) | Çalışır — dashboard kartları güncellendi |
| Aktif hata / blokaj | **Yok** — son istekler tamamlandı |

---

---

## Oturum: Gebelik Asistanı — OpenRouter, Çoklu Sohbet, UI (3 Haziran 2026)

### Yaklaşım

- **Mevcut mimari korundu:** `chat_messages` tablosu ve `/api/v1/chat` router’ı genişletildi; sıfırdan sayfa açılmadı, mevcut `BabyChat.tsx` (`/bebegimle-konus`) dönüştürüldü.
- **AI sağlayıcı:** OpenRouter (`openai/gpt-oss-120b:free`), `httpx` ile `POST /api/v1/chat/completions`, `reasoning: { enabled: true }`.
- **Bağlam seçimi:** Kullanıcı mesajı önce `analyze_message()` ile analiz edilir; genel gebelik sorularında `daily_logs` kullanılmaz, kişisel/belirti sorularında yalnızca ilgili alanlar (kilo, su, tansiyon, kan şekeri, nabız, not) çekilir.
- **Çoklu sohbet:** `chat_sessions` tablosu eklendi; her oturumda karşılama mesajı, sol panelde geçmiş, sağda aktif sohbet.
- **Dokümantasyon:** Proje kökünde `prodocs/` klasörü — Gebelik Asistanı mimarisi, OpenRouter, context seçimi, endpoint’ler, DB yapısı vb.

---

### Adım 1 — Backend: OpenRouter entegrasyonu ve asistan servisi

**Yapılanlar:**

| Dosya | Açıklama |
|--------|----------|
| `backend/app/services/openrouter_client.py` | OpenRouter API istemcisi |
| `backend/app/services/assistant_service.py` | Mesaj analizi, sistem promptları, sağlık bağlamı, karşılama metni |
| `backend/app/services/chat_service.py` | CRUD + `send_assistant_message()` |
| `backend/app/routers/chat_router.py` | Yeni endpoint’ler |
| `backend/.env` | `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `OPENROUTER_HTTP_REFERER`, `OPENROUTER_APP_TITLE` |

**Endpoint’ler (ilk sürüm):**
- `GET /chat/messages` — karşılama ile birlikte mesaj listesi
- `POST /chat/assistant` — kullanıcı mesajı + AI yanıtı

**AI davranış kuralları:** Türkçe, destekleyici ton, teşhis/ilaç yok, riskli belirtide doktora yönlendirme, gebelik haftasına göre yanıt.

---

### Adım 2 — Frontend: Mock sohbet → gerçek API

**Yapılanlar:**
- `BabyChat.tsx`: mock `setTimeout` kaldırıldı; API ile mesaj yükleme/gönderme
- `api.ts`: `getChatMessages()`, `sendAssistantMessage()`
- Sidebar ve Dashboard: “Bebeğimle Konuş” → **“Gebelik Asistanı”**; Dashboard CTA route’a bağlandı
- Karşılama mesajı backend’de otomatik: `Merhaba {ad} 👋`, `{hafta}. hafta`, vb.

---

### Adım 3 — Hata: 502 Bad Gateway (ASCII codec)

**Belirti:** Mesaj gönderince `502`, `ascii codec can't encode character '\u0131' in position 15`.

**Kök neden:** HTTP başlığı `X-Title: Gebelik Asistanı` içindeki Türkçe `ı`; Windows’ta `httpx`/httpcore başlıkları ASCII bekliyor.

**Çözüm:**
- `_ascii_header()` ile başlıklar ASCII’ye çevrildi
- JSON gövdesi `ensure_ascii=False` + UTF-8
- `.env`: `OPENROUTER_APP_TITLE=Gebelik Asistani`

**Sonuç:** OpenRouter çağrıları Windows’ta çalışır hale geldi.

---

### Adım 4 — UI: Sayfa boyutu ve iki sütunlu düzen

**İstek:** Sohbet alanı ortada çok küçük kalıyordu.

**Yapılanlar:**
- Container `max-w-3xl` → `max-w-[1400px]` (Dashboard/Forum ile aynı)
- Tam ekran yükseklik: `h-[calc(100dvh-4rem)]`, esnek kart yapısı

**Çoklu sohbet (sol panel + sağ chat):**

| Backend | Frontend |
|---------|----------|
| `chat_sessions` tablosu + `chat_messages.session_id` | Sol: Sohbet Geçmişi |
| Alembic migration `chat_sessions` | + Yeni Sohbet, liste, sil (çöp) ikonu |
| `GET/POST/DELETE /chat/sessions` | Sağ: aktif sohbet |
| `GET/POST .../sessions/{id}/messages` ve `.../assistant` | Başlık üstte tam genişlik; paneller başlığın altında |

Mevcut mesajlar migration ile kullanıcı başına “Sohbet 1” oturumuna taşındı.

---

### Adım 5 — UI: Sabit mesaj kutusu ve kaydırma

**Belirti:** Mesajlaştıkça giriş kutusu aşağı iniyordu; sohbet geçmişi paneli de sınırsız büyüyordu.

**Yapılanlar (`BabyChat.tsx`):**
- Sayfa `overflow-hidden` + sabit viewport yüksekliği
- **Sağ:** Mesajlar `overflow-y-auto` konteynerinde; form `shrink-0` ile altta sabit
- **Sol:** “Yeni Sohbet” sabit; liste `overflow-y-auto`
- `scrollIntoView` kaldırıldı → `messagesScrollRef` ile yalnızca mesaj alanı en alta kayıyor
- `AppLayout` `main`: `min-h-0 overflow-y-auto` (diğer sayfaların scroll’u bozulmasın diye)

**Sonuç:** Giriş kutusu sabit; mesajlar ve sohbet listesi kendi alanlarında kaydırılıyor.

---

### prodocs (referans dokümantasyon)

`prodocs/` altında: mimari, OpenRouter, sağlık verisi kullanımı, context seçimi, chat akışı, sistem promptları, güvenlik kuralları, backend endpoint’leri, veritabanı yapısı, `README.md`.

---

### Mevcut durum (Gebelik Asistanı)

| Bileşen | Durum |
|---------|--------|
| OpenRouter entegrasyonu | Çalışır (ASCII header düzeltmesi sonrası) |
| Çoklu sohbet oturumları | DB + API + UI tamam |
| İki sütunlu layout | Tamam |
| Sabit mesaj kutusu / iç scroll | Tamam |
| Aktif hata / blokaj | **Yok** — son UI scroll düzenlemesi tamamlandı |

---

### Sonraki olası adımlar — Gebelik Asistanı oturumu (henüz yapılmadı)

- OpenRouter API anahtarının rotate edilmesi (sohbette paylaşıldı)
- `prodocs` güncellemesi: `chat_sessions` endpoint’leri ve yeni UI
- Mobil görünümde sol panel yüksekliği ince ayarı (şu an `h-[220px]` mobil, `lg:h-full` masaüstü)
- Rate limiting / acil belirti anahtar kelime katmanı (dokümanda gelecek iyileştirme olarak not edildi)

---

## Oturum: Dashboard Bebek Verisi (weekly_metadata), Hero Metni, OpenRouter Boş Yanıt (3 Haziran 2026)

### Yaklaşım

- **Bebek kilo/boy:** Formül veya tahmin kullanma; tek kaynak `weekly_metadata` tablosu (`baby_weight`, `baby_length`, `baby_size`).
- **Hafta hesabı:** Kullanıcının SAT (`last_menstrual_period`) → `calculate_status()` ile gebelik haftası; dashboard bu haftaya göre ilgili satırı okur.
- **Veri doldurma:** Alembic migration ile tablo kontrolü + 1–42 hafta upsert; referans değerler `app/data/weekly_baby_reference.py` modülünde merkezi tutulur.
- **Hero özeti:** Meyve/nesne kıyası da aynı tablodan (`baby_size`); sabit kodlanmış hafta aralıkları kaldırıldı.
- **AI sohbet:** OpenRouter; boş `content` hatasında reasoning modu ve API yapılandırması incelenir.

---

### Adım 1 — Dashboard “Bebek Durumu” verisi nereden geliyor? (analiz)

**Soru:** Dashboard’daki bebek kilo/boy kartı hangi kaynaktan doluyor?

**Bulgu (eski durum):**
- Frontend: `Dashboard.tsx` → `apiClient.getDashboard()` → `summary_cards.baby`
- Backend: `ui_service.build_dashboard()`
- Hafta: kullanıcı SAT’ından
- Kilo/boy: önce `week * 32` / `week * 0.95` formülü; varsa `weekly_metadata` parse ediliyordu
- “Kilo Takibi” grafiği: annenin `daily_logs.weight` kayıtları (bebek kilosu değil)

**Sorun:** `seed.py` legacy alanları (`fetus_weight_gr`) dolduruyordu; entity modeli `baby_weight` / `baby_length` bekliyordu → tablo pratikte boş kalıyordu.

---

### Adım 2 — weekly_metadata: migration + seed + formül kaldırma

**İstek:** 1–42 hafta gerçekçi referans değerler; formül fallback yok; veri yoksa “Bilgi bulunamadı”.

**Yapılanlar:**

| Dosya | Açıklama |
|--------|----------|
| `backend/app/data/weekly_baby_reference.py` | 1–42 hafta tıbbi referanslara uygun yaklaşık boy/kilo/meyve (`baby_size`) |
| `backend/alembic/versions/weekly_metadata_baby_seed.py` | Tablo yoksa oluştur; 42 haftayı `ON CONFLICT (week_number) DO UPDATE` ile upsert |
| `backend/app/services/ui_service.py` | Formül kaldırıldı; doğrudan `baby_weight` / `baby_length` okunuyor |
| `backend/app/seed.py` | Legacy seed yerine `upsert_weekly_baby_metadata_session()` |
| `backend/tests/test_api.py` | Dashboard bebek kartının boş olmaması için assertion eklendi |

**Migration:** `alembic upgrade head` → `weekly_metadata_baby_seed` uygulandı; DB’de **42 kayıt** doğrulandı (ör. 12. hafta: `~14 g`, `5.4 cm`).

**Davranış:**
- Kayıt veya alan yoksa kart: `Bilgi bulunamadı` / `Boy: bilgi bulunamadı`

---

### Adım 3 — Hero metni: “Bebeğin bir nar büyüklüğünde…”

**Soru:** Dashboard hero `summary_text` nereden geliyor?

**Bulgu (eski durum):**
- `hero.summary_text` backend’de şablonla üretiliyordu
- Hafta: SAT’tan
- Meyve: `_comparison_for_week()` — sabit aralıklar (1–12 → hep “nar”); **weekly_metadata kullanılmıyordu**
- “ve seni duyabiliyor 💛” sabit cümle

**Yapılanlar (`ui_service.py`):**
- `_comparison_for_week()` kaldırıldı
- `weekly_metadata.baby_size` hero metnine bağlandı
- Örnek 5. hafta: “mercimek” (tablodaki değer)
- `baby_size` yoksa: “Bebeğinin büyüklük bilgisi bilgi bulunamadı”

---

### Adım 4 — Gebelik Asistanı: “AI yanıtı boş geldi” (502)

**Belirti:** Sohbette mesaj gönderince `POST /api/v1/chat/sessions/{id}/assistant` → **502 Bad Gateway**, hata metni: *“AI yanıtı boş geldi”*.

**Kök neden (analiz):**
- OpenRouter isteği 200 dönüyor ama `choices[0].message.content` boş kalabiliyor
- Kod `reasoning: { enabled: true }` gönderiyordu; bazı modeller yanıtı `reasoning` / `reasoning_content` alanına yazıp `content`’i boş bırakıyor
- Dashboard / weekly_metadata ile **ilgisi yok** — yalnızca OpenRouter yapılandırması ve istemci parse mantığı

**Olası ek nedenler:**
- `backend/.env` içinde geçersiz veya placeholder `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL=openai/gpt-oss-120b:free` kotası / geçici model hatası

**Yapılan düzeltme (`openrouter_client.py`):**
1. `reasoning: { enabled: true, exclude: true }` — cevabın `content` alanında gelmesi hedeflenir
2. `_extract_assistant_text()` — `content` boşsa `reasoning` / `reasoning_content` yedek okuma
3. Hata mesajına API anahtarı ve model kontrolü ipucu eklendi

**Gerekli `.env` alanları:**
```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-oss-120b:free
OPENROUTER_HTTP_REFERER=http://localhost:5173
OPENROUTER_APP_TITLE=Gebelik Asistani
```

---

### Mevcut durum (bu oturum)

| Bileşen | Durum |
|---------|--------|
| `weekly_metadata` 1–42 seed | Tamam — migration uygulandı |
| Dashboard bebek kilo/boy | Tablodan okunuyor, formül yok |
| Dashboard hero meyve kıyası | `baby_size` tablodan |
| OpenRouter boş yanıt | **Düzeltme uygulandı** — kullanıcı tarafında doğrulama bekleniyor |
| Aktif hata / blokaj | **Gebelik Asistanı 502** — `.env` API anahtarı / model kotası kontrol edilmeli; düzeltme sonrası sohbet tekrar denenecek |

---

### Sonraki olası adımlar (henüz yapılmadı)

- OpenRouter sohbetinin düzeltme sonrası uçtan uca testi (gerçek API anahtarı ile)
- `prodocs` güncellemesi: `weekly_metadata` seed, dashboard bebek verisi akışı, hero `baby_size`
- Hero metnindeki “seni duyabiliyor” gibi haftaya bağlı olmayan sabit cümlelerin haftalık içerikle zenginleştirilmesi (isteğe bağlı)
- `weekly_metadata` için `description` / `common_symptoms` alanlarının haftalık içerikle doldurulması (isteğe bağlı)

---

## Oturum: Kütüphane Markdown, Dashboard Grafik, Takvim TR, Forum Zamanı, Sağlık PDF Raporu (12–13 Haziran 2026)

### Yaklaşım

- **Kütüphane:** Supabase/backend’den gelen `body` alanı markdown; frontend’de `react-markdown` + `@tailwindcss/typography` (`prose`) ile HTML’e çevrildi.
- **Dashboard kilo grafiği:** X ekseni hamilelik haftası (`H5`) yerine ölçüm tarihi (`gg/aa`); backend `ui_service.build_dashboard()` güncellendi.
- **Takvim:** `react-day-picker` için varsayılan locale `date-fns/locale/tr` — günler ve aylar Türkçe.
- **Forum zaman etiketi:** Statik DB alanı `time_label` ("Az önce") yerine `created_at` üzerinden dinamik formatlama; önce göreli zaman, kullanıcı isteğiyle sadeleştirildi.
- **Sağlık PDF:** Mevcut `daily_logs` tablosu kullanıldı (yeni tablo gerekmedi); `GET /reports/pdf?start_date=&end_date=` + `reportlab` ile PDF üretimi; frontend’de tarih aralığı dialog’u.
- **PDF marka:** Sağ üst köşede uygulama adı + favicon tabanlı logo; sidebar ikonu denendi, kullanıcı geri aldı.

---

### Adım 1 — Kütüphane: Markdown ham metin olarak görünüyordu

**Belirti:** Makale içeriğinde `##`, `**`, `*` gibi işaretler düz metin olarak ekranda kalıyordu.

**Yapılanlar:**

| Dosya | Değişiklik |
|--------|------------|
| `frontend/package.json` | `react-markdown` eklendi |
| `frontend/src/pages/LibraryArticle.tsx` | `ReactMarkdown` ile `article.body` render |
| `frontend/tailwind.config.ts` | `@tailwindcss/typography` plugin etkinleştirildi |

---

### Adım 2 — Dashboard: Kilo grafiği X ekseni `H5` gösteriyordu

**İstek:** Yatay eksende kilonun girildiği tarih `gün/ay` formatında olsun.

**Yapılanlar:**

| Dosya | Değişiklik |
|--------|------------|
| `backend/app/services/ui_service.py` | `weight_points` artık `{"d": "15/03", "kg": ...}` — `created_at` tarihinden `strftime("%d/%m")` |
| `frontend/src/pages/Dashboard.tsx` | `XAxis dataKey="w"` → `dataKey="d"` |

---

### Adım 3 — Takvim: İngilizce gün ve ay adları

**Yapılanlar:**
- `frontend/src/components/ui/calendar.tsx` — `locale = tr` (`date-fns/locale`) varsayılan olarak `DayPicker`’a verildi
- Hafta Pazartesi’den başlar; hem Takvim sayfası hem kayıt ekranındaki tarih seçici etkilenir

---

### Adım 4 — Forum: Tüm sorular “Az önce” görünüyordu

**Kök neden:** `forum_threads.time_label` oluşturulurken `"Az önce"` yazılıyor ve API bu statik değeri döndürüyordu; `created_at` kullanılmıyordu.

**Yapılanlar (evrim):**

| Aşama | Davranış |
|--------|----------|
| İlk sürüm | `az önce` → `X dk önce` → `X saat önce` → `dün HH:MM` → `dd.MM.yyyy HH:MM` |
| Beyaz ekran | `formatRelativeTime.ts` içinde bozuk backtick → derleme hatası; string birleştirme ile düzeltildi |
| Kullanıcı sadeleştirmesi | Yalnızca: **Bugün saat HH:MM**, **Dün saat HH:MM**, eski kayıtlar **dd.MM.yyyy HH:MM** |

**Dosyalar:**
- `backend/app/core/time_format.py` — `format_relative_time_tr()`
- `backend/app/services/forum_service.py` — `_thread_time_label()` / `_reply_time_label()` `created_at`’ten hesaplıyor
- `frontend/src/lib/formatRelativeTime.ts` — aynı mantık + `useRelativeNow()` (gece yarısı geçişi için)
- `frontend/src/pages/Forum.tsx`, `ForumQuestion.tsx` — `created_at` ile formatlama

---

### Adım 5 — Sağlık Takibi: PDF raporu tarih aralığı ile indirme

**İstek:** “PDF Rapor Oluştur” tıklanınca tarih aralığı seçim penceresi; seçilen aralıktaki veriler PDF olarak indirilsin.

**Yapılanlar:**

| Katman | Dosya | Açıklama |
|--------|--------|----------|
| Backend | `health_service.py` | `list_daily_logs_in_range(user_id, start_date, end_date)` |
| Backend | `report_service.py` | `reportlab` ile tablo formatında PDF (`generate_report_pdf`) |
| Backend | `report_router.py` | `GET /api/v1/reports/pdf?start_date=&end_date=` |
| Backend | `requirements.txt` | `reportlab`, `pillow` eklendi |
| Frontend | `api.ts` | `downloadHealthReportPdf()` — blob indirme |
| Frontend | `HealthTracking.tsx` | Dialog: başlangıç/bitiş tarihi + “PDF raporunu indir” |

**PDF içeriği:** Tarih, kilo, tansiyon, şeker, su, nabız, not kolonları; aralıkta kayıt yoksa 404.

---

### Adım 6 — PDF: Uygulama adı ve logo (köşe markası)

**İstek:** PDF’de sağ üst köşede uygulama adı ve ikon.

**Yapılanlar:**
- `backend/app/assets/logo.svg` / `logo.png` — `frontend/public/favicon.svg` tabanlı
- `report_service.py` — `onFirstPage` / `onLaterPages` callback ile sağ üstte logo + “Bebeğim” / “Gebelik Takip”

**Sidebar ikon denemesi (geri alındı):**
- Sol bardaki yuvarlak Baby ikonunu PDF’e taşıma denendi (`sidebar-logo.svg` / `sidebar-logo.png`)
- Kullanıcı beğenmedi → `LOGO_PATH` tekrar `logo.png` (favicon) olarak ayarlandı

---

### Mevcut durum (bu oturum)

| Bileşen | Durum |
|---------|--------|
| Kütüphane markdown render | Tamam |
| Dashboard kilo grafiği tarih ekseni | Tamam (`gg/aa`) |
| Takvim Türkçe locale | Tamam |
| Forum zaman etiketi | Tamam (Bugün / Dün / tam tarih) |
| Sağlık PDF tarih aralığı | Tamam — backend endpoint + frontend dialog |
| PDF logo | **Favicon tabanlı eski logo** — sidebar ikonu geri alındı |
| Aktif hata / blokaj | **Yok** |

---

### Sonraki olası adımlar (henüz yapılmadı)

- PDF logo/marka görünümü için kullanıcı onaylı tasarım (sidebar ikonu veya favicon)
- Forum zaman formatının diğer sayfalarda (varsa) tutarlılık kontrolü
- Sağlık PDF’ine grafik özet veya kullanıcı gebelik haftası bilgisi eklenmesi (isteğe bağlı)
- `prodocs` güncellemesi: PDF rapor endpoint’i ve tarih aralığı akışı

---

