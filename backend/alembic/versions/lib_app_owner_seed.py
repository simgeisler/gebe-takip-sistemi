"""users: is_app_owner; seed library_articles

Revision ID: lib_app_owner_seed
Revises: cal_add_event_on
Create Date: 2026-05-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "lib_app_owner_seed"
down_revision: Union[str, Sequence[str], None] = "cal_add_event_on"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "is_app_owner",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    conn = op.get_bind()
    n = conn.execute(sa.text("SELECT COUNT(*) FROM library_articles")).scalar()
    if n and int(n) > 0:
        return

    rows = [
        {
            "category": "Beslenme",
            "title": "Hamilelikte dengeli beslenme",
            "description": "Günlük enerji, protein ve lif ihtiyacını nasıl karşılayabileceğinize dair pratik bir özet.",
            "read_minutes": 6,
            "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80",
            "body": (
                "Hamilelikte beslenme hem senin hem bebeğin için temel yapı taşlarını sağlar.\n\n"
                "Öğünlerinde tam tahıl, sebze, meyve, protein kaynağı (baklagil, yumurta, balık — "
                "doktorunun önerdiği güvenli seçenekler) ve sağlıklı yağlara yer ver.\n\n"
                "Bol su iç; işlenmiş gıda ve aşırı şekerden kaçın. Özel bir diyet veya risk "
                "durumunda mutlaka doktorun veya diyetisyeninle konuş."
            ),
        },
        {
            "category": "Hareket",
            "title": "Güvenli egzersiz ipuçları",
            "description": "Orta şiddette aktiviteyi nasıl sürdürebilirsin, nelere dikkat etmelisin?",
            "read_minutes": 5,
            "image_url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&q=80",
            "body": (
                "Doktorun onayıyla yürüyüş, hafif yoga veya yüzme gibi orta tempolu aktiviteler "
                "çoğu hamilelikte faydalı olabilir.\n\n"
                "Nefesini tutma, aşırı ısınma veya sert darbeler içeren sporlardan kaçın. "
                "Baş dönmesi, kanama veya keskin karın ağrısında aktiviteyi durdur ve hemen "
                "sağlık kuruluşuna başvur."
            ),
        },
        {
            "category": "Uyku",
            "title": "İkinci üç aylıkta uyku düzeni",
            "description": "Rahat pozisyonlar, gündüz yorgunluğu ve gece uykusunu iyileştirme.",
            "read_minutes": 4,
            "image_url": "https://images.unsplash.com/photo-1541781774459-bb2f2f5b9283?w=800&q=80",
            "body": (
                "Karın büyüdükçe yan yatış ve bacaklar arasına yastık koymak rahatlatır.\n\n"
                "Yatmadan önce ekranı azalt, odanı serin ve loş tut. Gerekirse gündüz kısa "
                "dinlenmeler planla; uzun gündüz uykusu geceyi zorlaştırabilir."
            ),
        },
        {
            "category": "Sağlık",
            "title": "Folik asit ve demir takviyeleri",
            "description": "Takviyeler hakkında bilmen gerekenler — doz ve zamanlama için doktorun rehberin.",
            "read_minutes": 5,
            "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474e2ae?w=800&q=80",
            "body": (
                "Folik asit, nöral tüp gelişimi için özellikle erken haftalarda önemlidir; "
                "demir ise artan kan hacmine destek olur.\n\n"
                "Hangi preparatı, hangi dozda kullanacağını mutlaka doktorun belirlemeli; "
                "kendi başına yüksek doz alımından kaçın."
            ),
        },
    ]

    for r in rows:
        conn.execute(
            sa.text(
                """
                INSERT INTO library_articles
                    (user_id, category, title, description, body, read_minutes, image_url)
                VALUES
                    (NULL, :category, :title, :description, :body, :read_minutes, :image_url)
                """
            ),
            r,
        )


def downgrade() -> None:
    op.drop_column("users", "is_app_owner")
