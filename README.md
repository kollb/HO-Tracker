# Home Office Tracker (Standalone)

Ein einfaches Tool zur Erfassung von Home Office- und Bürozeiten.
Es läuft **zu 100% im Browser** (kein Server, kein Python nötig) und speichert die Daten in einer lokalen JSON-Datei auf deinem Computer.

## ✨ Features

* **Intelligente Zeiterfassung:**
    * **Smart Input:** Tippe `0615` → wird automatisch `06:15`.
    * **Dynamische Endzeit:** Wähle "Büro" → Endzeit wird automatisch berechnet (Start + Sollzeit + Pause).
    * **Pausen-Logik:** Automatische Berechnung der Netto-Arbeitszeit inkl. gesetzlicher Pausenkorridore.
    * **Eingabe-Validierung:** Automatische Prüfung der Zeitangaben mit hilfreichen Fehlermeldungen.
* **Sonderregelungen (Neu):**
    * **Wäldchestag / Kurzarbeit:** Unterstützt Tage mit abweichender Sollzeit (z.B. 6h statt 7,8h).
    * **Eigene Feiertage:** Definiere betriebliche Ruhetage oder verkürzte Tage selbst.
* **Datenmanagement:**
    * **CSV Export:** Exportiere Monats- oder Jahresdaten als CSV-Datei für Excel/Sheets.
    * **Backup & Restore:** Sichere deine kompletten Daten und stelle sie bei Bedarf wieder her.
    * **Automatisches Speichern:** Änderungen werden sofort gespeichert (bei verbundener Datei).
* **Übersicht & Statistik:**
    * **Jahresansicht:** Balkendiagramm für das ganze Jahr.
    * **Budget:** Exakte Berechnung des Home Office Budgets (basierend auf den tatsächlichen Soll-Stunden des Monats).
    * **Druckansicht:** Optimierte Darstellung für den Druck.
    * **Dark Mode:** Augenschonend und standardmäßig aktiviert.
* **Tastenkombinationen:**
    * **Strg/Cmd + S:** Speichern
    * **Strg/Cmd + O:** Datei öffnen
    * **Strg/Cmd + E:** CSV exportieren
    * **← →:** Monat/Jahr wechseln
    * **1, 2, 3:** Ansicht wechseln (Liste/Kalender/Jahr)
    * **H:** Zum aktuellen Monat
    * **?:** Tastenkombinationen anzeigen

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
* **CSV Export:** Nutze das Download-Icon (⬇), um Daten als CSV zu exportieren - für Monat oder gesamtes Jahr.
* **Backup erstellen:** Öffne die Einstellungen und klicke auf "Backup herunterladen" für eine vollständige Sicherung.
* **Daten wiederherstellen:** In den Einstellungen kannst du ein Backup wiederherstellen.
* **Drucken:** Nutze die Druckfunktion deines Browsers (Strg/Cmd + P) für eine optimierte Druckansicht.
* **Zeiteingabe:** Du kannst Zeiten in verschiedenen Formaten eingeben:
  - `0815` wird automatisch zu `08:15`
  - `8:15` wird zu `08:15`
  - `8.15` wird zu `08:15`
* **Validierung:** Das System prüft deine Zeitangaben und warnt bei ungültigen Einträgen (z.B. Endzeit vor Startzeit).
* **Tastenkombinationen:** Drücke `?` um alle verfügbaren Tastenkombinationen anzuzeigen.

## 🛠 Technik

* **Vue.js 3 & Vuetify:** Für modernes, reaktives Design.
* **File System Access API:** Ermöglicht das direkte Schreiben in die lokale JSON-Datei (nur in Chromium-Browsern wie Chrome/Edge unterstützt).

## 🔧 Fehlerbehebung

**Datei lässt sich nicht öffnen/speichern:**
* Stelle sicher, dass du einen Chromium-basierten Browser verwendest (Chrome, Edge, Brave, etc.)
* Firefox und Safari unterstützen die File System Access API derzeit nicht vollständig
* Prüfe, ob du die Berechtigung zum Lesen/Schreiben der Datei erteilt hast

**Daten gehen verloren:**
* Die Daten werden im Browser-LocalStorage und (optional) in deiner JSON-Datei gespeichert
* Lösche nicht den Browser-Cache, wenn du die Datei nicht mit dem Tool verbunden hast
* Nutze regelmäßig den CSV-Export als Backup
* Erstelle Kopien deiner JSON-Datei als Sicherung

**Zeitvalidierung zeigt Fehler:**
* Endzeit muss nach der Startzeit liegen
* Zeiten müssen im 24-Stunden-Format sein (0-23 Stunden, 0-59 Minuten)
* Nutze das Format HH:MM (z.B. 08:00, 16:30)

**Browser-Kompatibilität:**
* ✅ Chrome/Chromium (ab Version 86)
* ✅ Edge (ab Version 86)
* ✅ Brave
* ⚠️ Firefox (eingeschränkt, LocalStorage funktioniert)
* ❌ Safari (File System Access API nicht unterstützt)

---
*Viel Erfolg beim Tracken!*
