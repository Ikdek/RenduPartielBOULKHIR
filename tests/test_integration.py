# TI
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_adherents():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/adherents")
    assert response.status_code == 200
    assert len(response.json()) >= 2

@pytest.mark.asyncio
async def test_create_reservation_api():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/reservations", params={
            "adherent_id": 2,
            "salle_id": 1,
            "sport_id": 1,
            "date": "2026-04-15",
            "schedule": "10:00-11:00"
        })
    assert response.status_code == 200
    assert response.json()["nom_adherent"] == "Alice Martin"

@pytest.mark.asyncio
async def test_insufficient_solde_api():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/reservations", params={
            "adherent_id": 1,
            "salle_id": 1,
            "sport_id": 2,
            "date": "2026-04-15",
            "schedule": "18:00-19:00"
        })
        assert response.status_code == 200
        await ac.post("/reservations", params={"adherent_id": 1, "salle_id": 1, "sport_id": 2, "date": "2026-04-15", "schedule": "19:00-20:00"})
        await ac.post("/reservations", params={"adherent_id": 1, "salle_id": 1, "sport_id": 2, "date": "2026-04-15", "schedule": "20:00-21:00"})
        response = await ac.post("/reservations", params={
            "adherent_id": 1,
            "salle_id": 1,
            "sport_id": 2,
            "date": "2026-04-15",
            "schedule": "21:00-22:00"
        })
        assert response.status_code == 400
        assert response.json()["detail"] == "Solde insuffisant"
