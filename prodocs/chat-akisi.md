# Chat Akışı

## İlk açılış

```
GET /api/v1/chat/messages
  → chat_service.list_messages()
  → ensure_welcome_message() — kayıt yoksa karşılama oluştur
  → [{ id, from: "baby", text: "Merhaba {ad} 👋..." }]
```

## Mesaj gönderme

```
POST /api/v1/chat/assistant  { "text": "..." }
  → ensure_welcome_message()
  → Kullanıcı mesajı flush (henüz commit yok)
  → analyze_message(text)
  → [personal_health ise] _fetch_health_context()
  → OpenRouter chat_completion()
  → Kullanıcı + asistan mesajları commit
  → { user_message, assistant_message }
```

## OpenRouter mesaj dizisi

```
[
  { role: "system", content: "SYSTEM_PROMPT + kullanıcı bağlamı [+ sağlık kayıtları]" },
  ...son 20 mesaj (me→user, baby→assistant),
  { role: "user", content: "yeni mesaj" }
]
```

## Frontend

1. Sayfa yüklenince `getChatMessages()` — geçmiş + karşılama.
2. Gönder → optimistik kullanıcı balonu → `sendAssistantMessage()`.
3. Başarılı → gerçek ID'li mesajlarla güncelle.
4. Hata → optimistik mesaj kaldır, toast göster.

## Route

- URL: `/bebegimle-konus` (değiştirilmedi, mevcut route korundu)
- Bileşen: `BabyChat.tsx`
