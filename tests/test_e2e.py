# E2E
import pytest
import threading
import uvicorn
import time
from playwright.sync_api import sync_playwright
from app.main import app

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

@pytest.fixture(scope="module", autouse=True)
def server():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(3)
    yield

def test_ui_reservation_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8001/static/index.html")
        page.wait_for_load_state("networkidle")
        page.select_option("#adherent", value="2")
        page.select_option("#salle", value="2")
        page.select_option("#sport", value="1")
        page.click("#btn-reserve")
        page.wait_for_selector(".success")
        assert "Réservation réussie" in page.inner_text("#status-message")
        page.wait_for_selector(".res-card")
        assert "Alice Martin" in page.inner_text("#reservations-list")
        browser.close()
