from datetime import date

import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import FCMToken


def run_weekly_push_job(database_url: str, firebase_credentials_json: str) -> None:
    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(firebase_credentials_json))

    engine = create_engine(database_url)
    with Session(engine) as db:
        tokens = [row.token for row in db.query(FCMToken).all()]
        for token in tokens:
            # Minimal MVP message; production'da kullanici bazli hafta metni olusturulabilir.
            message = messaging.Message(
                token=token,
                notification=messaging.Notification(
                    title="Yeni Gebelik Haftasi",
                    body=f"Bu hafta durumunuzu guncellemeyi unutmayin. Tarih: {date.today().isoformat()}",
                ),
            )
            messaging.send(message)


if __name__ == "__main__":
    # Example:
    # python weekly_notification_job.py postgresql+psycopg://... ./firebase-service-account.json
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("Usage: python weekly_notification_job.py <DATABASE_URL> <FIREBASE_CREDENTIALS_JSON>")
    run_weekly_push_job(sys.argv[1], sys.argv[2])
