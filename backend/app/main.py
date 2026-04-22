from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import SessionLocal, engine
from app.dependencies import init_firebase
from app.models import Base
from app.routers.content_routes import router as content_router
from app.routers.counter_routes import router as counter_router
from app.routers.log_routes import router as log_router
from app.routers.notification_routes import router as notification_router
from app.routers.profile_routes import router as profile_router
from app.routers.report_routes import router as report_router
from app.routers.status_routes import router as status_router
from app.seed import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_firebase()
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_data(db)
    yield


app = FastAPI(title="Gebelik Takibi MVP API", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(profile_router)
app.include_router(status_router)
app.include_router(log_router)
app.include_router(counter_router)
app.include_router(content_router)
app.include_router(report_router)
app.include_router(notification_router)
