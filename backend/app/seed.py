from sqlalchemy.orm import Session

from app.data.weekly_baby_reference import upsert_weekly_baby_metadata_session
from app.models import ForumCategory, LibraryItem
from app.models.entities import WeeklyMetadata


def seed_data(db: Session) -> None:
    if db.query(WeeklyMetadata).count() < 42:
        upsert_weekly_baby_metadata_session(db)

    if db.query(ForumCategory).count() == 0:
        for category_name in ["Hastane Onerileri", "Doktor Yorumlari", "Urun Tavsiyeleri"]:
            db.add(ForumCategory(name=category_name))
        db.commit()

    if db.query(LibraryItem).count() == 0:
        defaults = [
            ("Beslenme", "Gebelikte beslenme", "Protein ve su tuketimine dikkat edin."),
            ("Testler", "Zorunlu test takvimi", "Her trimester icin onerilen testleri takip edin."),
            ("Aktivite", "Guvenli egzersizler", "Dusuk yogunluklu yuruyus plani."),
            ("Yasal Haklar", "Dogum izni", "Calisan haklari ve izin surecleri."),
        ]
        for category, title, content in defaults:
            db.add(LibraryItem(category=category, title=title, content=content))
        db.commit()
