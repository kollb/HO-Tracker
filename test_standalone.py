import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000/ho-tracker.html"

# --- FIXTURE: Clean State ---
@pytest.fixture(autouse=True)
def clean_storage(page: Page):
    """Löscht vor jedem Test den LocalStorage."""
    page.goto(BASE_URL)
    page.evaluate("localStorage.clear()")
    page.reload()
    yield

# --- LOGIK TESTS ---
def test_js_normalize_time_input(page: Page):
    test_cases = [("830", "08:30"), ("08:00", "08:00"), ("9", "09:00"), ("2400", None)]
    for inp, expected in test_cases:
        result = page.evaluate(f"normalizeTimeInput('{inp}')")
        assert result == expected if expected else result is None

def test_js_calculate_net_hours(page: Page):
    # Angepasst an deine JS Logik (sofortiger Abzug)
    test_cases = [
        ("08:00", "12:00", 4.0),
        ("08:00", "14:00", 6.0),
        ("08:00", "14:05", 5.58),
        ("08:00", "17:00", 8.5),
    ]
    for start, end, expected in test_cases:
        result = page.evaluate(f"calculateNetHours('{start}', '{end}')")
        assert abs(result - expected) < 0.01

# --- GUI TESTS ---

def test_gui_create_standard_entry(page: Page):
    """Workflow: Standardeintrag erstellen."""
    page.locator("button:has(.mdi-pencil)").first.click()
    
    # Overlay & Typ "Büro" wählen
    overlay = page.locator(".v-overlay__content").filter(has=page.locator(".v-card")).filter(has_text="Home Office").first
    expect(overlay).to_be_visible()
    overlay.get_by_text("Büro", exact=True).click()
    
    # Auto-Fill Check
    expect(page.get_by_label("Start").last).to_have_value("08:00")
    
    page.get_by_text("Fertig").click()
    # Check auf Zahl (Einheit h kann getrennt sein)
    expect(page.locator("table")).to_contain_text("7,80")

def test_gui_split_entry(page: Page):
    """Workflow: Split Buchung."""
    
    # 1. Dialog öffnen
    page.locator("button:has(.mdi-pencil)").first.click()
    
    # 2. Ersten Eintrag ändern
    page.get_by_text("Home Office").click()
    
    # Ende ändern (Klick auf Titel nimmt Fokus sicher weg)
    page.locator(".v-card-title").click()
    end_input = page.get_by_label("Ende").first
    end_input.click()
    end_input.fill("12:00")
    end_input.press("Tab") # Change triggern
    
    # 3. Split hinzufügen
    page.get_by_text("Split hinzufügen").click()
    split_box = page.locator(".split-entry-box")
    expect(split_box).to_be_visible()
    
    # 4. Status wählen
    split_box.locator(".v-select").click()
    page.locator(".v-overlay__content").get_by_text("Büro").last.click()
    
    # 5. Zeiten füllen
    # Index 0 = Select, 1 = Start, 2 = Ende
    inputs = split_box.locator("input")
    
    # Start (13:00)
    start_in = inputs.nth(1)
    start_in.click(force=True)
    start_in.fill("13:00")
    start_in.press("Tab")
    
    # Ende (17:00)
    end_in = inputs.nth(2)
    end_in.click(force=True)
    end_in.fill("17:00")
    end_in.press("Tab")
    
    # Fokus wegnehmen zum Speichern
    page.locator(".v-card-title").click()
    
    # 6. Dialog schließen
    page.get_by_text("Fertig").click()
    
    # Prüfung: 4h + 4h = 8.00 h
    expect(page.locator("table")).to_contain_text("8,00")

def test_gui_settings_custom_holiday(page: Page):
    page.locator("button:has(.mdi-cog)").click()
    today = page.evaluate("new Date().toISOString().split('T')[0]")
    
    dialog = page.locator(".v-card").filter(has_text="Einstellungen")
    dialog.locator("input[type='date']").last.fill(today)
    dialog.get_by_label("Bez.").fill("TestFeiertag")
    dialog.get_by_label("Std.").fill("0")
    
    dialog.locator("button.v-btn--icon").last.click()
    page.get_by_text("Schließen").click()
    
    expect(page.locator("table")).to_contain_text("TestFeiertag")

def test_gui_switch_views(page: Page):
    page.locator("button[value='year']").click()
    expect(page.locator("th").filter(has_text="Urlaub")).to_be_visible()
    page.locator("button[value='list']").click()
    expect(page.locator("table")).to_be_visible()

def test_gui_pdf_import_dialog_check(page: Page):
    # Check ob Button & Input existieren
    expect(page.locator(".mdi-file-pdf-box")).to_be_visible()
    expect(page.locator("input[type='file']")).to_be_attached()
    
    # Prüfen ob der File Chooser aufgeht (Indiz für korrekte Verknüpfung)
    with page.expect_file_chooser(timeout=3000):
         page.locator("button:has(.mdi-file-pdf-box)").click()