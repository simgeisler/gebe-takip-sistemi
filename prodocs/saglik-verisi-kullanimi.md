# Kullanıcı Sağlık Verilerinin Kullanımı

Asistan, `daily_logs` tablosundaki kayıtlara erişebilir:

| Alan | DB kolonu |
|------|-----------|
| Kilo | `weight` |
| Günlük su tüketimi | `water_liters` |
| Sistolik tansiyon | `systolic` |
| Diyastolik tansiyon | `diastolic` |
| Kan şekeri | `blood_glucose` |
| Nabız | `pulse` |
| Notlar | `notes` |

## Ne zaman kullanılır?

Yalnızca kullanıcı **kişisel durum veya belirti** sorusu sorduğunda ve mesaj analizi ilgili alanları işaretlediğinde.

Genel gebelik sorularında (beslenme, bebek gelişimi, hafta bilgileri vb.) sağlık kayıtları **hiç çekilmez ve prompt'a eklenmez**.

## Veri kapsamı

- Son **10** kayıt (`created_at` / `date` sırasına göre)
- Yalnızca analiz sonucu seçilen alanlar formatlanır
- Kayıt yoksa asistana "ilgili sağlık kaydı bulunmuyor" bilgisi verilir

## Kullanıcı profili

Her istekte (genel veya kişisel) sistem prompt'una eklenir:

- Ad (`users.name`)
- Gebelik haftası (`last_menstrual_period` → `calculate_status()`)
- Trimester
