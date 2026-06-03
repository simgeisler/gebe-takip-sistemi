"""Gebelik Asistanı — mesaj analizi, bağlam seçimi ve OpenRouter entegrasyonu."""

import re
from dataclasses import dataclass, field
from typing import Literal

from sqlalchemy.orm import Session

from ..core.pregnancy import calculate_status
from ..models.entities import ChatMessage, ChatSession, DailyLog, User
from .openrouter_client import chat_completion

Role = Literal["baby", "me"]
HealthField = Literal["weight", "water", "blood_pressure", "glucose", "pulse", "notes"]

MAX_HISTORY = 20
MAX_LOG_ENTRIES = 10

# Kişisel / belirti sorularında sağlık verisi kategorileri
_FIELD_KEYWORDS: dict[HealthField, tuple[str, ...]] = {
    "weight": (
        "kilo", "kilom", "kilo art", "kilo ald", "tartı", "tarti", "ağırlık", "agirlik",
        "zayıf", "zayif", "şişman", "sisman", "kilo kayb",
    ),
    "water": (
        "su tüket", "su tuket", "su iç", "su ic", "susuz", "dehidrasyon", "litre", "hydration",
    ),
    "blood_pressure": (
        "tansiyon", "sistolik", "diyastolik", "kan basınc", "kan basinc", "hipertans",
        "hipotans", "baş dön", "bas don", "baş ağr", "bas agr",
    ),
    "glucose": (
        "kan şeker", "kan seker", "glukoz", "glucose", "şeker", "seker", "diyabet", "gestasyonel",
    ),
    "pulse": (
        "nabız", "nabiz", "kalp at", "çarpınt", "carpint", "taşikardi", "tasikardi", "ritim",
    ),
    "notes": (
        "notum", "notlarım", "notlarim", "kaydettim", "yazdım", "yazdim",
    ),
}

# Genel gebelik konuları — kişisel belirti yoksa sağlık kaydı kullanılmaz
_GENERAL_KEYWORDS = (
    "beslen", "vitamin", "bebek geliş", "bebek gelis", "fetal", "trimester", "trimester",
    "doğum", "dogum", "emzir", "egzersiz", "spor", "uyku pozisyon", "hafta bebek",
    "bebeğim ne kadar", "bebegim ne kadar", "ultrason", "amniyosentez", "genel bilgi",
    "nasıl büyür", "nasil buyur", "organ", "kalp atışı bebek", "tekmeler ne zaman",
)

# Kişisel / belirti göstergeleri
_PERSONAL_SYMPTOM_KEYWORDS = (
    "halsiz", "yorgun", "mide bulant", "kusma", "ağrı", "agri", "kramp", "kanama",
    "leke", "ödem", "od em", "şişlik", "sislik", "nefes dar", "iştah", "istah",
    "hisset", "hissediyorum", "hissediyor", "durumum", "belirti", "semptom", "normal mi",
    "kayd", "verilerim", "ölçüm", "olcum", "değerlerim", "degerlerim", "son ölç",
    "başım", "basim", "midem", "karnım", "karnim", "sırt", "sirt", "bacak",
)


@dataclass
class MessageAnalysis:
    mode: Literal["general", "personal_health"] = "general"
    fields: list[HealthField] = field(default_factory=list)


def analyze_message(text: str) -> MessageAnalysis:
    """Kullanıcı mesajını analiz eder; genel mi kişisel sağlık mı ve hangi alanlar gerekli."""
    normalized = text.lower()
    normalized = re.sub(r"\s+", " ", normalized)

    matched_fields: list[HealthField] = []
    for field_name, keywords in _FIELD_KEYWORDS.items():
        if any(kw in normalized for kw in keywords):
            matched_fields.append(field_name)

    has_personal = any(kw in normalized for kw in _PERSONAL_SYMPTOM_KEYWORDS)
    has_general_only = any(kw in normalized for kw in _GENERAL_KEYWORDS)

    if matched_fields or has_personal:
        fields = matched_fields or ["weight", "water", "blood_pressure", "glucose", "pulse", "notes"]
        return MessageAnalysis(mode="personal_health", fields=fields)

    if has_general_only:
        return MessageAnalysis(mode="general", fields=[])

    # Belirsiz sorular: genel kabul et (sağlık kaydı ekleme)
    return MessageAnalysis(mode="general", fields=[])


def build_welcome_text(user: User) -> str:
    status = calculate_status(user.last_menstrual_period)
    week = status["week"]
    return (
        f"Merhaba {user.name} 👋\n"
        f"Gebeliğinin şu anda {week}. haftasındasın.\n"
        "Gebelik sürecin, bebeğinin gelişimi veya sağlık kayıtların hakkında bana soru sorabilirsin."
    )


def add_welcome_message(user_id: int, session_id: int, db: Session) -> None:
    """Yeni sohbet oturumuna karşılama mesajı ekler."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    row = ChatMessage(
        user_id=user_id,
        session_id=session_id,
        role="baby",
        text=build_welcome_text(user),
    )
    db.add(row)


def create_session_with_welcome(user_id: int, db: Session) -> ChatSession:
    """Yeni sohbet oturumu ve karşılama mesajı oluşturur."""
    session = ChatSession(user_id=user_id, title="Yeni Sohbet")
    db.add(session)
    db.flush()
    add_welcome_message(user_id, session.id, db)
    db.commit()
    db.refresh(session)
    return session


def _format_log_entry(log: DailyLog, fields: list[HealthField]) -> str:
    parts = [f"Tarih: {log.date.isoformat()}"]
    if "weight" in fields and log.weight is not None:
        parts.append(f"Kilo: {log.weight} kg")
    if "water" in fields and log.water_liters is not None:
        parts.append(f"Su: {log.water_liters} L")
    if "blood_pressure" in fields and log.systolic is not None and log.diastolic is not None:
        parts.append(f"Tansiyon: {log.systolic}/{log.diastolic} mmHg")
    if "glucose" in fields and log.blood_glucose is not None:
        parts.append(f"Kan şekeri: {log.blood_glucose} mg/dL")
    if "pulse" in fields and log.pulse is not None:
        parts.append(f"Nabız: {log.pulse} bpm")
    if "notes" in fields and log.notes:
        parts.append(f"Not: {log.notes}")
    return " | ".join(parts)


def _fetch_health_context(user_id: int, fields: list[HealthField], db: Session) -> str:
    if not fields:
        return ""
    logs = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id)
        .order_by(DailyLog.date.desc(), DailyLog.id.desc())
        .limit(MAX_LOG_ENTRIES)
        .all()
    )
    if not logs:
        return "Kullanıcının ilgili sağlık kaydı bulunmuyor."

    lines = [_format_log_entry(log, fields) for log in logs]
    relevant = [line for line in lines if line.count("|") > 0 or "Not:" in line]
    if not relevant:
        return "Kullanıcının ilgili sağlık kaydı bulunmuyor."
    return "Son sağlık kayıtları:\n" + "\n".join(f"- {line}" for line in relevant)


SYSTEM_PROMPT = """Sen "Gebelik Asistanı"sın — hamilelik sürecinde bilgilendirici ve destekleyici bir yapay zeka asistanısın.

KURALLAR:
- Her zaman Türkçe yanıt ver.
- Anlaşılır, sıcak ve destekleyici ol.
- Teşhis koyma, ilaç önerme veya doktor yerine geçme.
- Riskli belirtilerde (şiddetli kanama, yoğun ağrı, bayılma, ciddi nefes darlığı vb.) mutlaka doktora veya acil sağlık kuruluşuna başvurulmasını öner.
- Tıbbi tavsiye vermiyorsun; genel bilgilendirme ve destek sağlıyorsun.
- Kullanıcının gebelik haftasını dikkate al.
- Genel gebelik sorularında sağlık kayıtlarını kullanma veya bahsetme.
- Kişisel durum veya belirti sorularında yalnızca sana verilen sağlık kayıtlarını referans al; kayıt yoksa bunu belirt.
- Yanıtlarını kısa ve net tut (genelde 2–4 paragraf)."""


def _build_openrouter_messages(
    user: User,
    history: list[ChatMessage],
    user_text: str,
    analysis: MessageAnalysis,
    health_context: str,
) -> list[dict]:
    status = calculate_status(user.last_menstrual_period)
    user_context = (
        f"Kullanıcı: {user.name}\n"
        f"Gebelik haftası: {status['week']}\n"
        f"Trimester: {status['trimester']}\n"
        f"Soru türü: {'kişisel sağlık / belirti' if analysis.mode == 'personal_health' else 'genel gebelik bilgisi'}"
    )

    system_parts = [SYSTEM_PROMPT, user_context]
    if analysis.mode == "personal_health" and health_context:
        system_parts.append(f"\n{health_context}")

    messages: list[dict] = [{"role": "system", "content": "\n\n".join(system_parts)}]

    for row in history[-MAX_HISTORY:]:
        role = "user" if row.role == "me" else "assistant"
        messages.append({"role": role, "content": row.text})

    messages.append({"role": "user", "content": user_text})
    return messages


def generate_assistant_reply(
    user_id: int,
    session_id: int,
    user_text: str,
    db: Session,
) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Kullanıcı bulunamadı.")

    analysis = analyze_message(user_text)
    health_context = ""
    if analysis.mode == "personal_health":
        health_context = _fetch_health_context(user_id, analysis.fields, db)

    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id, ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id)
        .all()
    )

    messages = _build_openrouter_messages(user, history, user_text, analysis, health_context)
    return chat_completion(messages)
