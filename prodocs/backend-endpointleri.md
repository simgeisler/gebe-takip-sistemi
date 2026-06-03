# Backend Endpointleri

Tüm endpoint'ler prefix: `/api/v1/chat`

Kimlik doğrulama: `Authorization: Bearer <token>`

## GET /messages

Sohbet geçmişini listeler. İlk açılışta karşılama mesajı otomatik oluşturulur.

**Yanıt:**
```json
[
  { "id": 1, "from": "baby", "text": "Merhaba Ayşe 👋\n..." },
  { "id": 2, "from": "me", "text": "24. haftada neler olur?" }
]
```

## POST /assistant

Kullanıcı mesajı gönderir, AI yanıtı üretir. **Ana asistan endpoint'i.**

**İstek:**
```json
{ "text": "Son tansiyon değerlerim normal mi?" }
```

**Yanıt:**
```json
{
  "user_message": { "id": 3, "from": "me", "text": "..." },
  "assistant_message": { "id": 4, "from": "baby", "text": "..." }
}
```

## POST /messages

Manuel mesaj oluşturma (CRUD — legacy / test).

**İstek:**
```json
{ "from": "me", "text": "..." }
```

## PUT /messages/{message_id}

Mesaj metnini günceller.

## DELETE /messages/{message_id}

Mesaj siler.

## Hata kodları

| Kod | Durum |
|-----|-------|
| 400 | Boş mesaj, geçersiz `from` |
| 401 | Geçersiz / eksik token |
| 502 | OpenRouter hatası |
| 503 | API anahtarı yapılandırılmamış |
| 504 | AI zaman aşımı |
