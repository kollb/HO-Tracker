# Home Office Tracker (Standalone)

Ein einfaches Tool zur Erfassung von Home Office- und Bürozeiten.
Es läuft **zu 100% im Browser** (kein Server, kein Python nötig) und speichert die Daten in einer lokalen JSON-Datei auf deinem Computer.

## ✨ Features

* **Intelligente Zeiterfassung:**
    * **Smart Input:** Tippe `0615` → wird automatisch `06:15`.
    * **Dynamische Endzeit:** Wähle "Büro" → Endzeit wird automatisch berechnet (Start + Sollzeit + Pause).
    * **Pausen-Logik:** Automatische Berechnung der Netto-Arbeitszeit inkl. gesetzlicher Pausenkorridore.
* **Sonderregelungen (Neu):**
    * **Wäldchestag / Kurzarbeit:** Unterstützt Tage mit abweichender Sollzeit (z.B. 6h statt 7,8h).
    * **Eigene Feiertage:** Definiere betriebliche Ruhetage oder verkürzte Tage selbst.
* **Übersicht & Statistik:**
    * **Jahresansicht:** Balkendiagramm für das ganze Jahr.
    * **Budget:** Exakte Berechnung des Home Office Budgets (basierend auf den tatsächlichen Soll-Stunden des Monats).
    * **Dark Mode:** Augenschonend und standardmäßig aktiviert.

## 🚀 Installation & Start

1.  **Datei ablegen:**
    Speichere die `ho-tracker.html` irgendwo auf deinem PC (z.B. Desktop oder Dokumente).

2.  **Daten-Datei erstellen:**
    Erstelle eine leere Textdatei namens `daten.json` am gewünschten Speicherort.

3.  **Starten:**
    Öffne `ho-tracker.html` mit einem modernen Browser (Chrome, Edge).

4.  **Verbinden:**
    Klicke oben rechts auf das **Ordner-Icon** 📂 und wähle deine `meine_daten.json` aus.
    *Der Browser wird dich um Erlaubnis fragen, die Datei zu bearbeiten. Bestätige dies.*

## 💡 Nutzungstipps

* **Wäldchestag:** Gehe in die Einstellungen (Zahnrad) und klicke auf "Wäldchestag hinzufügen", um ihn für das aktuelle Jahr mit 6h Sollzeit einzutragen.
* **Navigation:** Klicke auf den Titel "Home Office Tracker", um schnell zum aktuellen Monat zurückzukehren.
* **Sortierung:** "Home Office" steht in der Auswahlliste immer ganz oben für schnellen Zugriff.

## 🛠 Technik

* **Vue.js 3 & Vuetify:** Für modernes, reaktives Design.
* **File System Access API:** Ermöglicht das direkte Schreiben in die lokale JSON-Datei (nur in Chromium-Browsern wie Chrome/Edge unterstützt).

---
*Viel Erfolg beim Tracken!*
