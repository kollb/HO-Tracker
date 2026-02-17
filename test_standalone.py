import pytest
from playwright.sync_api import Page, expect
import re

BASE_URL = "http://localhost:8000/ho-tracker.html"

# --- HELPER ---
def fill_and_trigger(page: Page, label: str, value: str):
    """Füllt Input robust aus."""
    inp = page.get_by_label(label).first
    inp.click()
    inp.fill(value)
    inp.press("Tab")

# --- TEIL 1: LOGIK TESTS ---

def test_js_normalize_time_input(page: Page):
    """Prüft, ob Zeiteingaben wie '830' korrekt zu '08:30' werden."""
    page.goto(BASE_URL)
    test_cases = [("830", "08:30"), ("08:00", "08:00"), ("1730", "17:30"), ("9", "09:00")]
    for inp, expected in test_cases:
        result = page.evaluate(f"normalizeTimeInput('{inp}')")
        assert result == expected, f"Input '{inp}' failed. Got '{result}'"

def test_js_calculate_net_hours(page: Page):
    """Prüft die gesetzliche Pausenregelung."""
    page.goto(BASE_URL)
    test_cases = [
        ("08:00", "14:00", 6.0),
        ("08:00", "14:30", 6.0),
        ("08:00", "17:00", 8.5),
        ("08:00", "18:00", 9.25)
    ]
    for start, end, expected in test_cases:
        result = page.evaluate(f"calculateNetHours('{start}', '{end}')")
        assert abs(result - expected) < 0.01, f"{start}-{end} failed. Got {result}"

# --- TEIL 2: GUI TESTS ---

def test_gui_create_standard_entry(page: Page):
    """
    Testet den Standard-Workflow: Klick "Büro" -> Speichern.
    Prüft, ob die Standardberechnung (7,8h) übernommen wird.
    """
    page.goto(BASE_URL)
    
    # 1. Dialog öffnen
    page.locator("button:has(.mdi-pencil)").first.click()
    
    # 2. Typ "Büro" wählen
    page.get_by_text("Büro", exact=True).click()
    
    # 3. Speichern
    page.get_by_text("Fertig").click()
    
    # 4. Prüfen (7,80 h ist Standard bei 39h Woche)
    expect(page.locator("body")).to_contain_text("7,80 h")
    
    # Aufräumen (Löschen)
    page.locator("button:has(.mdi-pencil)").first.click()
    fill_and_trigger(page, "Start", "")
    page.get_by_text("Fertig").click()
    expect(page.locator("body")).not_to_contain_text("7,80 h")

def test_gui_verify_initial_autofill(page: Page):
    """
    Testet die 'Intelligenz': Beim Klick auf den Status müssen 
    Start- und Endzeit automatisch berechnet und eingetragen werden.
    """
    page.goto(BASE_URL)
    
    # 1. Dialog öffnen
    page.locator("button:has(.mdi-pencil)").first.click()
    
    # 2. "Home Office" klicken. Das sollte Zeiten triggern.
    page.get_by_text("Home Office").click()
    
    # 3. Prüfen: Start muss 08:00 sein (Standard)
    start_input = page.get_by_label("Start").first
    expect(start_input).to_have_value("08:00")
    
    # 4. Prüfen: Ende muss berechnet sein.
    # Bei 39h Woche (7.8h Tag) + 0.5h Pause = 8.3h Anwesenheit.
    # 08:00 + 8.3h = 16:18.
    end_input = page.get_by_label("Ende").first
    expect(end_input).to_have_value("16:18")

def test_gui_settings_weekend_toggle(page: Page):
    """Testet das Ausblenden der Wochenenden."""
    page.goto(BASE_URL)
    expect(page.locator("body")).to_contain_text("Sa")
    
    page.locator("button:has(.mdi-cog)").click()
    page.get_by_text("Wochenenden ausblenden").click()
    page.get_by_text("Schließen").click()
    
    # Wieder einschalten
    page.locator("button:has(.mdi-cog)").click()
    page.get_by_text("Wochenenden ausblenden").click()
    page.get_by_text("Schließen").click()
    
    expect(page.locator("body")).to_contain_text("Sa")

def test_gui_series_planner(page: Page):
    """Testet den Serienplaner Workflow."""
    page.goto(BASE_URL)
    page.locator("button:has(.mdi-calendar-multiple)").first.click()
    
    dialog = page.get_by_role("dialog")
    expect(dialog.get_by_text("Serien-Planer")).to_be_visible()
    
    dialog.locator(".v-select").click()
    page.get_by_text("Urlaub").first.click()
    
    dialog.get_by_text("Ausführen").click()
    expect(page.locator(".v-snackbar__content")).to_contain_text("geplant")