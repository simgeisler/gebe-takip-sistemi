# Sistem Promptları

## Ana sistem promptu

Tanım: `assistant_service.SYSTEM_PROMPT`

İçerik özeti:

- Rol: Gebelik Asistanı — bilgilendirici ve destekleyici
- Dil: Türkçe
- Teşhis koyma, ilaç önerme, doktor yerine geçme yasak
- Riskli belirtilerde acil/doktor yönlendirmesi
- Gebelik haftasına göre yanıt
- Genel sorularda sağlık kaydı kullanmama
- Kişisel sorularda yalnızca verilen kayıtları referans alma

## Dinamik bağlam (system mesajına eklenir)

```
Kullanıcı: {name}
Gebelik haftası: {week}
Trimester: {trimester}
Soru türü: genel gebelik bilgisi | kişisel sağlık / belirti
```

## Sağlık kaydı bloğu (yalnızca personal_health)

```
Son sağlık kayıtları:
- Tarih: 2026-05-01 | Kilo: 68.5 kg | Tansiyon: 120/80 mmHg
- ...
```

## Karşılama mesajı

Şablon (`build_welcome_text`):

```
Merhaba {kullanıcı_adı} 👋
Gebeliğinin şu anda {gebelik_haftası}. haftasındasın.
Gebelik sürecin, bebeğinin gelişimi veya sağlık kayıtların hakkında bana soru sorabilirsin.
```

Karşılama statik bir prompt değil; kullanıcı adı ve hafta DB'den hesaplanır, `chat_messages`'a `role=baby` olarak kaydedilir.
