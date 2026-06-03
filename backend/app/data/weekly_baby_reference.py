"""
Haftalık fetal boy/kilo referans verileri (1–42. gebelik haftası).

Yaklaşık ortalama değerler; klinik ultrason ve gebelik gelişim tablolarındaki
yaygın referans aralıklarına uyumludur (erken haftalarda CRL, 20. haftadan sonra
taç-topuk uzunluğu ve tahmini fetal ağırlık).
"""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.entities import WeeklyMetadata

# (week, weight_display, length_cm, size_comparison_tr)
_REFERENCE: list[tuple[int, str, str, str]] = [
    (1, "<1 g", "0,1 cm", "tohum"),
    (2, "<1 g", "0,2 cm", "haşhaş tohumu"),
    (3, "<1 g", "0,3 cm", "susam"),
    (4, "<1 g", "0,4 cm", "susam"),
    (5, "<1 g", "0,5 cm", "mercimek"),
    (6, "<1 g", "0,6 cm", "mercimek"),
    (7, "1 g", "1,0 cm", "yaban mersini"),
    (8, "1 g", "1,6 cm", "ahududu"),
    (9, "2 g", "2,3 cm", "üzüm"),
    (10, "4 g", "3,1 cm", "çilek"),
    (11, "7 g", "4,1 cm", "incir"),
    (12, "14 g", "5,4 cm", "erik"),
    (13, "23 g", "7,4 cm", "şeftali"),
    (14, "43 g", "8,7 cm", "limon"),
    (15, "70 g", "10,1 cm", "elma"),
    (16, "100 g", "11,6 cm", "avokado"),
    (17, "140 g", "13,0 cm", "armut"),
    (18, "190 g", "14,2 cm", "dolmalık biber"),
    (19, "240 g", "15,3 cm", "mango"),
    (20, "300 g", "25,6 cm", "muz"),
    (21, "360 g", "26,7 cm", "havuç"),
    (22, "430 g", "27,8 cm", "papaya"),
    (23, "501 g", "28,9 cm", "greyfurt"),
    (24, "600 g", "30,0 cm", "mısır"),
    (25, "660 g", "34,6 cm", "karnabahar"),
    (26, "760 g", "35,6 cm", "marul"),
    (27, "875 g", "36,6 cm", "kış kabağı"),
    (28, "1,0 kg", "37,6 cm", "patlıcan"),
    (29, "1,15 kg", "38,6 cm", "kabak"),
    (30, "1,32 kg", "39,9 cm", "lahana"),
    (31, "1,50 kg", "41,1 cm", "hindistan cevizi"),
    (32, "1,70 kg", "42,4 cm", "hindistan cevizi"),
    (33, "1,92 kg", "43,7 cm", "ananas"),
    (34, "2,15 kg", "45,0 cm", "kavun"),
    (35, "2,38 kg", "46,2 cm", "kavun"),
    (36, "2,62 kg", "47,4 cm", "marul başı"),
    (37, "2,86 kg", "48,6 cm", "pazı"),
    (38, "3,08 kg", "49,8 cm", "pırasa"),
    (39, "3,29 kg", "50,7 cm", "karpuz"),
    (40, "3,46 kg", "51,2 cm", "karpuz"),
    (41, "3,50 kg", "51,5 cm", "karpuz"),
    (42, "3,55 kg", "51,7 cm", "karpuz"),
]


def _build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for week, weight, length, size in _REFERENCE:
        rows.append(
            {
                "week_number": week,
                "title": f"{week}. Hafta",
                "baby_weight": f"~{weight}",
                "baby_length": length.replace(",", "."),
                "baby_size": size,
            }
        )
    return rows


WEEKLY_BABY_ROWS: list[dict[str, Any]] = _build_rows()

NOT_FOUND_LABEL = "Bilgi bulunamadı"


def upsert_weekly_baby_metadata_session(db: Session) -> None:
    for row in WEEKLY_BABY_ROWS:
        week_number = row["week_number"]
        existing = (
            db.query(WeeklyMetadata)
            .filter(WeeklyMetadata.week_number == week_number)
            .first()
        )
        if existing:
            existing.title = row.get("title")
            existing.baby_weight = row.get("baby_weight")
            existing.baby_length = row.get("baby_length")
            existing.baby_size = row.get("baby_size")
        else:
            db.add(WeeklyMetadata(**row))
    db.commit()


def upsert_weekly_baby_metadata_connection(connection) -> None:
    import sqlalchemy as sa

    for row in WEEKLY_BABY_ROWS:
        connection.execute(
            sa.text(
                """
                INSERT INTO weekly_metadata
                    (week_number, title, baby_weight, baby_length, baby_size)
                VALUES
                    (:week_number, :title, :baby_weight, :baby_length, :baby_size)
                ON CONFLICT (week_number) DO UPDATE SET
                    title = EXCLUDED.title,
                    baby_weight = EXCLUDED.baby_weight,
                    baby_length = EXCLUDED.baby_length,
                    baby_size = EXCLUDED.baby_size
                """
            ),
            row,
        )


def ensure_weekly_metadata_table(op) -> None:
    """Alembic: tablo yoksa mevcut entity şemasıyla oluşturur."""
    import sqlalchemy as sa
    from sqlalchemy import inspect

    bind = op.get_bind()
    if "weekly_metadata" in inspect(bind).get_table_names():
        return

    op.create_table(
        "weekly_metadata",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("week_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("baby_size", sa.String(), nullable=True),
        sa.Column("baby_weight", sa.String(), nullable=True),
        sa.Column("baby_length", sa.String(), nullable=True),
        sa.Column("common_symptoms", sa.Text(), nullable=True),
        sa.Column("tips", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("week_number"),
    )
    op.create_index("ix_weekly_metadata_id", "weekly_metadata", ["id"], unique=False)
    op.create_index(
        "ix_weekly_metadata_week_number", "weekly_metadata", ["week_number"], unique=True
    )
