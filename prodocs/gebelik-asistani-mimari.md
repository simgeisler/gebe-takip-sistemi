# Gebelik Asistanı — Genel Mimari

Gebelik Asistanı, kullanıcıların gebelik süreci hakkında soru sorabildiği AI destekli bir sohbet özelliğidir.

## Bileşenler

```
Frontend (BabyChat.tsx)
    ↓ REST API
Backend (chat_router → chat_service → assistant_service)
    ↓                    ↓
chat_messages DB    OpenRouter API
    ↑
daily_logs DB (koşullu)
```

## Akış özeti

1. Kullanıcı `/bebegimle-konus` sayfasını açar.
2. `GET /chat/messages` sohbet geçmişini döner; kayıt yoksa karşılama mesajı oluşturulur.
3. Kullanıcı mesaj yazar → `POST /chat/assistant`.
4. Backend mesajı analiz eder, gerekirse sağlık verilerini çeker, OpenRouter'a gönderir.
5. AI yanıtı `chat_messages` tablosuna kaydedilir ve frontend'e döner.

## Dosya konumları

| Katman | Dosya |
|--------|-------|
| Router | `backend/app/routers/chat_router.py` |
| Chat CRUD + orchestration | `backend/app/services/chat_service.py` |
| AI mantığı | `backend/app/services/assistant_service.py` |
| OpenRouter istemcisi | `backend/app/services/openrouter_client.py` |
| Frontend | `frontend/src/pages/BabyChat.tsx` |

## Rol eşlemesi

- `me` → kullanıcı mesajı
- `baby` → AI asistan yanıtı (legacy isimlendirme, UI'da "Gebelik Asistanı")
