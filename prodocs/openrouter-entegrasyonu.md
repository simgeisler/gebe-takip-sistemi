# OpenRouter Entegrasyonu

Gebelik Asistanı, LLM çağrıları için [OpenRouter](https://openrouter.ai/) kullanır.

## Ortam değişkenleri

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `OPENROUTER_API_KEY` | API anahtarı | — (zorunlu) |
| `OPENROUTER_MODEL` | Model adı | `openai/gpt-oss-120b:free` |
| `OPENROUTER_HTTP_REFERER` | OpenRouter referer header | `http://localhost:5173` |
| `OPENROUTER_APP_TITLE` | Uygulama adı header | `Gebelik Asistanı` |

## İstemci

`backend/app/services/openrouter_client.py` — `httpx` ile `POST /api/v1/chat/completions` çağrısı yapar.

```python
chat_completion(messages, reasoning_enabled=True)
```

Reasoning modu etkin (`reasoning: { enabled: true }`). Yanıt metni `choices[0].message.content` alanından okunur.

## Hata yönetimi

- API anahtarı yok → HTTP 503
- Zaman aşımı (90 sn) → HTTP 504
- OpenRouter / ağ hatası → HTTP 502

## Not

Reasoning detayları (`reasoning_details`) veritabanına kaydedilmez; sohbet geçmişi yalnızca metin içeriğiyle yeniden oluşturulur.
