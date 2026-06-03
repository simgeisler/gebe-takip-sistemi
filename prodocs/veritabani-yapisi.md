# Veritabanı Yapısı

## chat_messages

Mevcut tablo (`add_remaining_tables` migration) — yeni migration gerekmedi.

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| `id` | Integer PK | Mesaj ID |
| `user_id` | Integer FK → `users.id` | Mesaj sahibi |
| `role` | String | `me` (kullanıcı) veya `baby` (asistan) |
| `text` | Text | Mesaj içeriği |
| `created_at` | DateTime TZ | Oluşturulma zamanı |

## İlişkiler

```
users (1) ──< (N) chat_messages
users (1) ──< (N) daily_logs
```

- Her kullanıcının kendi sohbet geçmişi vardır.
- Karşılama mesajı da `chat_messages`'da `role=baby` olarak saklanır.

## daily_logs (sağlık verisi)

Asistan tarafından okunur; chat tablosuna yazılmaz.

| Kolon | Kullanım |
|-------|----------|
| `weight` | Kilo |
| `water_liters` | Su tüketimi |
| `systolic` / `diastolic` | Tansiyon |
| `blood_glucose` | Kan şekeri |
| `pulse` | Nabız |
| `notes` | Notlar |

## users (profil)

| Kolon | Asistan kullanımı |
|-------|-------------------|
| `name` | Karşılama + prompt |
| `last_menstrual_period` | Gebelik haftası hesabı |

## Model dosyası

`backend/app/models/entities.py` — `ChatMessage`, `DailyLog`, `User`
