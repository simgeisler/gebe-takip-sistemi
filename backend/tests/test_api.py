from datetime import date, timedelta

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_auth_register_and_login_flow():
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "last_menstrual_period": "2025-10-10",
        "starting_weight": 63.5,
    }
    register_res = client.post("/api/v1/auth/register", json=payload)
    assert register_res.status_code == 200
    token = register_res.json()["access_token"]
    assert token

    login_res = client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()


def test_dashboard_and_frontend_shapes():
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Elif Yıldız",
            "email": "elif.shape@example.com",
            "password": "password123",
            "last_menstrual_period": "2025-09-10",
            "starting_weight": 62.0,
        },
    )
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}

    dash = client.get("/api/v1/dashboard", headers=h)
    assert dash.status_code == 200
    d = dash.json()
    assert "hero" in d and "summary_cards" in d
    assert "weight_chart" in d and "upcoming" in d
    assert "baby" in d["summary_cards"]

    lib = client.get("/api/v1/library/articles")
    assert lib.status_code == 200
    articles = lib.json()
    assert len(articles) >= 1
    assert "cat" in articles[0] and "desc" in articles[0] and "time" in articles[0] and "id" in articles[0]

    forum = client.get("/api/v1/forum/threads")
    assert forum.status_code == 200
    threads = forum.json()
    assert len(threads) >= 1
    t0 = threads[0]
    assert "cat" in t0 and "author" in t0 and "votes" in t0 and "id" in t0

    chat = client.get("/api/v1/chat/messages", headers=h)
    assert chat.status_code == 200
    msgs = chat.json()
    assert len(msgs) >= 1
    assert msgs[0]["from"] in ("baby", "me") and "text" in msgs[0]


def test_dashboard_upcoming_shows_nearest_two_calendar_events():
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Dash Upcoming",
            "email": "dash.up@example.com",
            "password": "password123",
            "last_menstrual_period": "2025-09-10",
            "starting_weight": 60.0,
        },
    )
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    d0 = (date.today() + timedelta(days=1)).isoformat()
    d1 = (date.today() + timedelta(days=2)).isoformat()
    d2 = (date.today() + timedelta(days=3)).isoformat()

    for payload in (
        {"day": "Pzt", "date": 1, "event_on": d2, "title": "En uzak", "time": "12:00", "type": "etkinlik"},
        {"day": "Sal", "date": 2, "event_on": d0, "title": "Birinci", "time": "09:00", "type": "ilac"},
        {"day": "Çar", "date": 3, "event_on": d1, "time": "10:00", "type": "randevu", "title": "İkinci"},
    ):
        r = client.post("/api/v1/calendar/events", headers=headers, json=payload)
        assert r.status_code == 200

    dash = client.get("/api/v1/dashboard", headers=headers)
    assert dash.status_code == 200
    up = dash.json()["upcoming"]
    assert len(up) == 2
    assert up[0]["title"] == "Birinci"
    assert up[1]["title"] == "İkinci"
    assert up[0]["tag"] == "İlaç"
    assert up[1]["tag"] == "Randevu"


def test_calendar_upcoming_measurements_crud():
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Planner User",
            "email": "planner@example.com",
            "password": "password123",
            "last_menstrual_period": "2025-09-10",
            "starting_weight": 58.0,
        },
    )
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    ev = client.get("/api/v1/calendar/events", headers=headers)
    assert ev.status_code == 200
    assert len(ev.json()) >= 1

    new_ev = client.post(
        "/api/v1/calendar/events",
        headers=headers,
        json={
            "day": "Pzt",
            "date": 12,
            "title": "Test",
            "time": "10:00",
            "type": "ilac",
        },
    )
    assert new_ev.status_code == 200
    eid = new_ev.json()["id"]

    upd = client.put(
        f"/api/v1/calendar/events/{eid}",
        headers=headers,
        json={"title": "Test güncellendi"},
    )
    assert upd.status_code == 200
    assert upd.json()["title"] == "Test güncellendi"

    rem = client.get("/api/v1/upcoming/", headers=headers)
    assert rem.status_code == 200
    assert len(rem.json()) >= 1

    nr = client.post(
        "/api/v1/upcoming/",
        headers=headers,
        json={
            "title": "Vitamin",
            "time": "08:00",
            "tag": "İlaç",
            "color": "bg-accent/20 text-foreground",
        },
    )
    assert nr.status_code == 200
    rid = nr.json()["id"]

    assert client.delete(f"/api/v1/upcoming/{rid}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/calendar/events/{eid}", headers=headers).status_code == 200

    m = client.post(
        "/api/v1/measurements/",
        headers=headers,
        json={
            "date": "2026-01-15",
            "weight_kg": 60.0,
            "systolic": 118,
            "diastolic": 76,
            "blood_glucose_mg_dl": 90,
            "pulse": 72,
            "water_liters": 1.5,
            "notes": "test",
        },
    )
    assert m.status_code == 200
    mid = m.json()["id"]
    charts = client.get("/api/v1/measurements/charts", headers=headers)
    assert charts.status_code == 200
    c = charts.json()
    assert "tansiyon" in c and "kilo" in c and "seker" in c
    assert client.delete(f"/api/v1/measurements/{mid}", headers=headers).status_code == 200


def test_future_measurement_blocked():
    register_res = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Log User",
            "email": "log@example.com",
            "password": "password123",
            "last_menstrual_period": "2025-09-10",
            "starting_weight": 58.1,
        },
    )
    token = register_res.json()["access_token"]
    future_date = date(2100, 1, 1).isoformat()
    log_res = client.post(
        "/api/v1/measurements/",
        headers={"Authorization": f"Bearer {token}"},
        json={"date": future_date, "weight_kg": 60.2},
    )
    assert log_res.status_code == 400
