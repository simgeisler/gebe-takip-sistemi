# Context Seçim Mantığı

Mesaj analizi `assistant_service.analyze_message()` fonksiyonunda yapılır.

## Modlar

| Mod | Açıklama |
|-----|----------|
| `general` | Genel gebelik bilgisi — sağlık kaydı kullanılmaz |
| `personal_health` | Kişisel durum / belirti — seçili alanlar DB'den çekilir |

## Karar süreci

1. Mesaj küçük harfe çevrilir ve normalize edilir.
2. **Alan anahtar kelimeleri** taranır (kilo, tansiyon, su, kan şekeri, nabız, not).
3. **Kişisel belirti kelimeleri** taranır (halsizlik, ağrı, durumum, ölçüm vb.).
4. Eşleşme varsa → `personal_health` + eşleşen alanlar.
5. Yalnızca genel gebelik kelimeleri varsa → `general`.
6. Belirsiz sorular → `general` (güvenli varsayılan).

## Alan eşlemesi

| Alan | Örnek tetikleyiciler |
|------|---------------------|
| `weight` | kilo, tartı, kilo artışı |
| `water` | su tüketimi, susuzluk |
| `blood_pressure` | tansiyon, baş dönmesi |
| `glucose` | kan şekeri, glukoz |
| `pulse` | nabız, çarpıntı |
| `notes` | notlarım, kaydettim |

Kişisel belirti var ama spesifik alan eşleşmezse tüm alanlar sorgulanır.

## Genişletme

Anahtar kelime listeleri `_FIELD_KEYWORDS`, `_PERSONAL_SYMPTOM_KEYWORDS`, `_GENERAL_KEYWORDS` sabitlerinde tanımlıdır (`assistant_service.py`).
