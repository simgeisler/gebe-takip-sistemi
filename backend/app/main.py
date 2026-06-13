from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse, Response

app = FastAPI(title="Bebeğim- Gebelik Takip API", version="0.1.0")

API_PREFIX = "/api/v1"

# CORS TEK VE DOĞRU
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://gebe-takip-sistemi.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from .routers.auth_router import router as auth_router
from .routers.calendar_router import router as calendar_router
from .routers.chat_router import router as chat_router
from .routers.dashboard_router import router as dashboard_router
from .routers.forum_extended import router as forum_extended_router
from .routers.forum_router import router as forum_router
from .routers.library_extended import router as library_extended_router
from .routers.health_extended import router as health_extended_router
from .routers.measurements_router import router as measurements_router
from .routers.notification_router import router as notification_router
from .routers.report_router import router as report_router
from .routers.upcoming_router import router as upcoming_router
from .routers.wellbeing_router import router as wellbeing_router



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

for router in (
    auth_router,
    calendar_router,
    chat_router,
    dashboard_router,
    forum_router,
    measurements_router,
    forum_extended_router,
    library_extended_router,
    health_extended_router,
    notification_router,
    report_router,
    upcoming_router,
    wellbeing_router,
):
    app.include_router(router, prefix=API_PREFIX)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "api": API_PREFIX}
