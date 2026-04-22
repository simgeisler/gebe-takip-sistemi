from sqlalchemy.orm import Session

from app.models import ForumCategory, LibraryItem, WeeklyMetadata


def seed_data(db: Session) -> None:
    if db.query(WeeklyMetadata).count() == 0:
        for week_number in range(1, 43):
            db.add(
                WeeklyMetadata(
                    week_number=week_number,
                    fetus_size_cm=round(0.2 * week_number + 1.4, 2),
                    fetus_weight_gr=round(6.5 * week_number * week_number + 20, 2),
                    development_milestones_json={"week": week_number, "summary": f"{week_number}. hafta gelisim ozeti"},
                    symptom_analysis_text=f"{week_number}. haftada gorulebilecek belirtiler.",
                    comparison_object_name=f"Referans Nesne {week_number}",
                    image_url=f"https://example.com/weeks/{week_number}.png",
                )
            )
        db.commit()

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
