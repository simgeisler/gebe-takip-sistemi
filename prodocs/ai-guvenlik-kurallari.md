# AI Güvenlik Kuralları

Gebelik Asistanı aşağıdaki kurallara uymak üzere yapılandırılmıştır.

## Davranış kuralları

| Kural | Uygulama |
|-------|----------|
| Türkçe yanıt | Sistem prompt'unda zorunlu |
| Destekleyici ton | Sistem prompt'unda |
| Teşhis koymama | Sistem prompt'unda yasak |
| İlaç önermeme | Sistem prompt'unda yasak |
| Doktor yerine geçmeme | Sistem prompt'unda yasak |
| Riskli belirti yönlendirmesi | Sistem prompt'unda (acil / doktor) |
| Sağlık verisini gerektiğinde kullanma | Context seçim mantığı + prompt |
| Genel sorularda kayıt eklememe | `analyze_message()` + prompt |

## Frontend uyarısı

Sayfa altında sabit metin:

> Gebelik Asistanı tıbbi tavsiye vermez. Acil durumlarda doktorunuza veya acil servise başvurun.

## Veri minimizasyonu

- Genel sorularda `daily_logs` sorgulanmaz.
- Kişisel sorularda yalnızca eşleşen alanlar formatlanır.
- Sohbet geçmişi kullanıcıya özel (`user_id` filtresi).

## API güvenliği

Tüm chat endpoint'leri JWT (`Authorization: Bearer`) gerektirir.

## Gelecek iyileştirmeler

- Acil belirti anahtar kelimeleri için ek kural katmanı
- Rate limiting
- İçerik filtreleme / moderation API
