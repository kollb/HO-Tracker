import pytest
import os
import re
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000/ho-tracker.html"
PRIVATE_DIR = "testfiles"

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
    test_cases = [
        ("08:00", "12:00", 4.0),
        ("08:00", "14:00", 6.0),
        ("08:00", "14:05", 6.0),   
        ("08:00", "14:30", 6.0),   
        ("08:00", "15:00", 6.5),   
        ("08:00", "17:00", 8.5),   
        ("08:00", "17:35", 9.0),   
        ("08:00", "18:00", 9.25),  
    ]
    for start, end, expected in test_cases:
        result = page.evaluate(f"calculateNetHours('{start}', '{end}')")
        assert abs(result - expected) < 0.01

# --- GUI TESTS ---
def test_gui_create_standard_entry(page: Page):
    row = page.locator(".day-row").first
    row.hover()
    row.locator(".mdi-pencil").click()
    
    overlay = page.locator(".v-overlay__content").filter(has_text="Home Office").first
    expect(overlay).to_be_visible()
    overlay.get_by_text("Büro", exact=True).click()
    
    expect(page.get_by_label("Startzeit").first).to_have_value("08:00")
    
    # ANGEPASST: Sucht jetzt nach dem neuen Label "Gleitzeit Saldo"
    override_input = page.get_by_label("Gleitzeit Saldo")
    expect(override_input).to_be_visible()
    override_input.fill("12.5")
    override_input.press("Tab")
    
    page.get_by_text("Schließen").click()
    
    expect(page.locator("table").first).to_contain_text("7,80")
    expect(page.locator("table").first).to_contain_text("+12,50")
    
    # ANGEPASST: Sucht nach dem neuen PDF Icon (statt mdi-anchor)
    expect(page.locator("table").locator(".mdi-file-pdf-box").first).to_be_visible()

def test_gui_split_entry(page: Page):
    row = page.locator(".day-row").first
    row.hover()
    row.locator(".mdi-pencil").click()
    
    dialog = page.locator(".v-overlay__content").filter(has_text="Schließen").first
    dialog.get_by_text("Home Office", exact=True).first.click()
    
    end_input = page.get_by_label("Endzeit").first
    end_input.click()
    end_input.fill("12:00")
    end_input.press("Tab")
    
    page.get_by_text("Split hinzufügen").click()
    
    start_inputs = dialog.get_by_label("Startzeit")
    end_inputs = dialog.get_by_label("Endzeit")
    
    start_inputs.nth(1).fill("13:00")
    start_inputs.nth(1).press("Tab")
    end_inputs.nth(1).fill("17:00")
    end_inputs.nth(1).press("Tab")
    
    page.get_by_text("Schließen").click()
    expect(page.locator("table").first).to_contain_text("8,00")

def test_gui_settings_custom_holiday(page: Page):
    page.locator(".v-list-item").filter(has_text="Einstellungen").click()
    today = page.evaluate("new Date().toISOString().split('T')[0]")
    
    dialog = page.locator(".v-overlay__content").filter(has_text="Einstellungen")
    dialog.locator("input[type='date']").first.fill(today)
    dialog.get_by_label("Bez.").fill("TestFeiertag")
    dialog.get_by_label("Std.").fill("0")
    
    dialog.locator(".mdi-content-save").locator("..").click()
    expect(dialog.get_by_text("TestFeiertag").first).to_be_visible()
    
    dialog.locator("div.d-flex.align-center").filter(has_text="TestFeiertag").locator(".mdi-pencil").click()
    dialog.get_by_label("Bez.").fill("Geändert")
    dialog.locator(".mdi-content-save").locator("..").click()
    
    expect(dialog.get_by_text("Geändert").first).to_be_visible()
    
    page.get_by_text("Speichern & Schließen").click()
    expect(page.locator("table").first).to_contain_text("Geändert")

def test_gui_switch_views(page: Page):
    expect(page.locator(".status-bar").first).to_be_visible()
    
    page.locator(".v-list-item").filter(has_text="Jahresübersicht").click()
    expect(page.locator("th").filter(has_text="Urlaub")).to_be_visible()
    expect(page.locator("canvas#donutChart")).to_be_attached()
    
    page.locator(".v-list-item").filter(has_text="Listenansicht").click()
    expect(page.locator("table").first).to_be_visible()

def test_gui_pdf_import_dialog_check(page: Page):
    pdf_path = os.path.join(PRIVATE_DIR, "standard.pdf")
    if not os.path.exists(pdf_path):
        pytest.skip("Private PDF fehlt.")

    page.goto(BASE_URL)
    page.locator('input[type="file"][accept=".pdf"]').set_input_files(pdf_path)
    expect(page.get_by_text("PDF Import (Lokal)")).to_be_visible()

def test_pdf_import_standard_month(page: Page):
    pdf_path = os.path.join(PRIVATE_DIR, "standard.pdf")
    if not os.path.exists(pdf_path):
        pytest.skip("Private PDF 'standard.pdf' nicht gefunden.")

    page.goto(BASE_URL)
    page.locator('input[type="file"][accept=".pdf"]').set_input_files(pdf_path)

    page.get_by_text("Import starten").click()
    expect(page.locator(".v-snackbar__content")).to_contain_text("importiert")

    page.evaluate("window.vm.currentDate = new Date(2025, 5, 1); window.vm.loadMonthData();")
    
    row = page.locator("tr").filter(has_text="2. Mo").first
    expect(row).to_contain_text("Home Office")
    expect(row.locator("input").nth(1)).to_have_value("07:40")
    expect(row.locator("input").nth(2)).to_have_value("16:30")

def test_pdf_import_missing_booking(page: Page):
    pdf_path = os.path.join(PRIVATE_DIR, "error.pdf")
    if not os.path.exists(pdf_path):
        pytest.skip("Private PDF 'error.pdf' nicht gefunden.")

    page.goto(BASE_URL)
    page.locator('input[type="file"][accept=".pdf"]').set_input_files(pdf_path)
    
    page.get_by_text("Import starten").click()
    expect(page.locator(".v-snackbar__content")).to_contain_text("importiert")

    page.evaluate("window.vm.currentDate = new Date(2026, 1, 1); window.vm.loadMonthData();")

    row = page.locator("tr").filter(has_text="13. Fr").first
    comment_field = row.locator("input").last
    expect(comment_field).to_have_value(re.compile("Buchung fehlt", re.IGNORECASE))

def test_pdf_import_overwrite_checkbox(page: Page):
    pdf_path = os.path.join(PRIVATE_DIR, "standard.pdf")
    if not os.path.exists(pdf_path):
        pytest.skip("Private PDF fehlt.")

    page.goto(BASE_URL)
    page.locator('input[type="file"][accept=".pdf"]').set_input_files(pdf_path)
    
    dialog = page.get_by_text("PDF Import (Lokal)")
    expect(dialog).to_be_visible()
    
    checkbox = page.get_by_label("Existierende Einträge überschreiben")
    checkbox.click()
    
    page.get_by_text("Import starten").click()
    expect(page.locator(".v-snackbar__content")).to_contain_text("importiert")